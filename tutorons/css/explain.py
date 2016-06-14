#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import re
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl as TerminalNode

from tutorons.common.java.gateway import java_isinstance
from tutorons.common.java.simplenlg import factory as nlg_factory,\
    Feature, NumberAgreement, Form, NPPhraseSpec
from parsers.css.CssLexer import CssLexer
from parsers.css.CssParser import CssParser
from parsers.css.CssListener import CssListener
from parsers.common.util import parse_plaintext, walk_tree


logging.basicConfig(level=logging.INFO, format="%(message)s")


def explain(selector):
    explainer = CssExplainer()
    try:
        parse_tree = parse_plaintext(selector, CssLexer, CssParser, 'selectors_group')
        walk_tree(parse_tree, explainer)
        return explainer.result
    except Exception:
        # Although this is a pretty broad catch, we want the default
        # behavior of explanation to be that the program continues to
        # run, even if one selector was not properly explained.
        return None


# Convenience function for getting the unique identifier of a node that the
# walker is currently visiting that can be used to hash results
_key = lambda ctx: ctx.invokingState


def explain_attribute(attribute_node):

    EQUALITY_SYMBOLS = [
        CssLexer.PREFIXMATCH,
        CssLexer.SUFFIXMATCH,
        CssLexer.SUBSTRINGMATCH,
        CssLexer.EQUALS,
        CssLexer.INCLUDES,
        CssLexer.DASHMATCH,
    ]

    EQUALITY_SYMBOL_VERBS = {
        CssLexer.PREFIXMATCH: 'start with',
        CssLexer.SUFFIXMATCH: 'end with',
        CssLexer.SUBSTRINGMATCH: 'contain',
        CssLexer.EQUALS: 'equal',
        CssLexer.INCLUDES: 'include',
        CssLexer.DASHMATCH: 'start with',
    }

    ATTRIBUTE_SUBJECTS = {
        'href': 'link',
    }

    state = 'seeking attribute'
    attribute_name = None
    equality_operation = None
    value = None

    for child in attribute_node.children:
        if (state == 'seeking attribute' and
                isinstance(child, TerminalNode) and
                child.symbol.type == CssLexer.IDENTIFIER):
            attribute_name = child.getText()
            state = 'seeking equality'
        elif (state == 'seeking equality' and
                isinstance(child, TerminalNode) and
                child.symbol.type in EQUALITY_SYMBOLS):
            equality_operation = child.symbol.type
            state = 'seeking value'
        elif (state == 'seeking value' and
                isinstance(child, TerminalNode) and
                child.symbol.type in [CssLexer.IDENTIFIER, CssLexer.STRING]):
            value = child.getText()
            state = 'found all'

    clause = nlg_factory.createClause()
    verb = nlg_factory.createVerbPhrase('have')
    clause.setVerb(verb)

    if attribute_name in ATTRIBUTE_SUBJECTS:
        object_ = nlg_factory.createNounPhrase(ATTRIBUTE_SUBJECTS[attribute_name])
    else:
        object_ = nlg_factory.createNounPhrase('attribute')
        object_.addPreModifier("'" + attribute_name + "'")
    object_.setDeterminer('a')
    clause.setObject(object_)

    value_clause = nlg_factory.createClause()
    value_verb = nlg_factory.createVerbPhrase(EQUALITY_SYMBOL_VERBS[equality_operation])
    value_clause.setVerb(value_verb)

    # Surround the value in quotation marks if it isn't already within them
    value_string = value if re.match('^(".*"|\'.*\')$', value) else "'" + value + "'"
    value_object_ = nlg_factory.createNounPhrase(value_string)
    value_clause.setObject(value_object_)

    clause.setComplement(value_clause)

    return clause


def explain_class(class_node):

    clause = nlg_factory.createClause()

    verb = nlg_factory.createVerbPhrase('belong to')
    clause.setVerb(verb)

    object_ = nlg_factory.createNounPhrase("'" + class_node.children[1].getText() + "'")
    object_.addPreModifier('class')
    clause.setObject(object_)

    return clause


def explain_hash(hash_node):

    clause = nlg_factory.createClause()

    verb = nlg_factory.createVerbPhrase('have')
    clause.setVerb(verb)

    hash_name = hash_node.children[0].getText()[1:]
    object_ = nlg_factory.createNounPhrase("'" + hash_name + "'")
    object_.addPreModifier('ID')
    clause.setObject(object_)

    return clause


def explain_type_selector(type_selector_node):

    def _lookup_type_name(type_):
        TYPE_NAMES = {
            'p': 'paragraph',
            'div': 'container',
            'strong': 'bolded text segment',
            'a': 'link',
            'img': 'image',
            'pre': 'preformatted text block',
            'table': 'HTML table',
            'tr': 'table row',
            'td': 'table cell',
        }
        return TYPE_NAMES.get(type_, type_)

    # A selector chooses all elements that match a specification.
    # Here, we build up this description of "all elements"
    noun = nlg_factory.createNounPhrase('element')

    # Look up a 'fancier' name for this element, if we can
    type_ = type_selector_node.children[-1].getText()
    type_name = _lookup_type_name(type_)

    # Only reset the type of noun ('element') to the type name
    # if we were able to find a more specificname during lookup.
    if type_name != type_:
        noun.setNoun(type_name)
    else:
        noun.addPreModifier('\'' + _lookup_type_name(type_) + '\'')

    # Make sure to plurarlize the count
    noun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)

    return noun


def explain_universal(universal_node):
    noun = nlg_factory.createNounPhrase('element')
    noun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
    return noun


def explain_pseudoclass(pseudo_node):

    # This is a list of pseudo-classes that are already adjectives and do
    # not have to be converted by lookup into adjectives.
    ADJECTIVE_PSEUDOCLASSES = [
        'checked',
        'hidden',
        'visible',
        'enabled',
        'active',
        'empty',
        'visited',
    ]

    # This is a lookup table from pseudoclasses to descriptions of the
    # conditions where elements are selected.
    PSEUDOCLASS_ADJECTIVES = {
        'hover': 'hovered over',
        'focus': 'focused',
    }

    clause = nlg_factory.createClause()
    functionalPseudo = pseudo_node.getChild(0, CssParser.Functional_pseudoContext)
    if functionalPseudo is not None:
        # Here's where we need to make a bunch of custom rules for different
        # functional pseudo-classes, as each of them have some pretty involved
        # behavior that's not very easy to describe with English.
        # For now we settle with a pretty simple and very vague default.
        verb = nlg_factory.createVerbPhrase('satisfy')
        clause.setVerb(verb)
        object_ = nlg_factory.createNounPhrase("'" + functionalPseudo.getText() + "'")
        object_.addPreModifier('function')
        object_.setDeterminer('the')
        clause.setObject(object_)
    else:
        pseudoclass = pseudo_node.children[1].getText()
        clause.setVerb('be')
        if pseudoclass in ADJECTIVE_PSEUDOCLASSES:
            adjective = nlg_factory.createAdjectivePhrase(pseudoclass)
        else:
            adjective = nlg_factory.createAdjectivePhrase(PSEUDOCLASS_ADJECTIVES[pseudoclass])
        clause.setObject(adjective)

    return clause


def explain_pseudoelement(pseudo_node):

    pseudoelement_name = pseudo_node.children[2].getText()

    # Given the small list of pseudo-elements supported by CSS3,
    # this section shows manual authoring of micro-explanations for each one.
    noun = nlg_factory.createNounPhrase()

    if pseudoelement_name == 'before':
        noun.setNoun('content')
        noun.addPreModifier('generated')
        preposition = nlg_factory.createPrepositionPhrase("before the element's content")
        noun.addComplement(preposition)
    else:
        noun.setNoun('content')
        verb = nlg_factory.createVerbPhrase('match')
        verb.setFeature(Feature.FORM, Form.PRESENT_PARTICIPLE)
        object_ = nlg_factory.createNounPhrase("'" + pseudo_node.getText() + "'")
        object_.setPreModifier('pseudo-element')
        object_.setDeterminer('the')
        description_clause = nlg_factory.createClause()
        description_clause.setVerb(verb)
        description_clause.setObject(object_)
        noun.addPostModifier(description_clause)

    return noun


def explain_pseudo(pseudo_node):
    '''
    Returns:
    * if the pseudo structure is a pseudo-class, this returns a
    clause describing the conditions where elements get selected.
    * if the pseduo structure is a pseudo-element, this returns a noun
    describing the content that is selected
    '''

    colon_count = 0
    for child in pseudo_node.children:
        if isinstance(child, TerminalNode) and child.symbol.type == CssLexer.COLON:
            colon_count += 1
            if colon_count >= 2:
                break

    pseudo_type = 'class' if colon_count == 1 else 'element'
    if pseudo_type == 'class':
        return explain_pseudoclass(pseudo_node)
    elif pseudo_type == 'element':
        return explain_pseudoelement(pseudo_node)


def explain_simple_selector_sequence(simple_selector_sequence_node, focus=True):
    '''
    Arguments:
    * simple_selector_sequence_node: subtree of syntax tree for a
        simple_selector_sequence_node symbol.
    * focus: whether this is the main simple selector sequence (i.e. the end
        of a list of simple selector sequences)
    '''
    clause = nlg_factory.createNounPhrase()
    tag_determiner = simple_selector_sequence_node.children[0]

    if isinstance(tag_determiner, CssParser.Type_selectorContext):
        noun = explain_type_selector(tag_determiner)
    elif isinstance(tag_determiner, CssParser.UniversalContext):
        noun = explain_universal(tag_determiner)
    if focus is True:
        noun.addPreModifier('all')
    clause.setNoun(noun)

    # Each selector in the sequence produces another layer of specificity.
    # In this loop, we accrue descriptions of what each selector is doing,
    # so that we can append them into a joined list at the end to describe
    # the entire sequence.
    pseudoelement_phrase = None
    modifiers = []
    for selector in simple_selector_sequence_node.children[1:]:
        if isinstance(selector, CssParser.PseudoContext):
            modifier = explain_pseudo(selector)
            # If this is a noun, then we have found a pseudo-element, which
            # needs to be described as the subject, not a modifier.
            if java_isinstance(modifier, NPPhraseSpec):
                pseudoelement_phrase = modifier
                modifier = None
        elif isinstance(selector, CssParser.AttributeContext):
            modifier = explain_attribute(selector)
        elif isinstance(selector, CssParser.Class_Context):
            modifier = explain_class(selector)
        elif isinstance(selector, CssParser.Hash_Context):
            modifier = explain_hash(selector)

        if modifier is not None:
            # Coerce all child phrases to describe multiple elements insteada
            # of just one element.  Centralizes this operation.
            modifier.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
            modifiers.append(modifier)

    # Add all of the modifiers from the individual selectors into a
    # coordinated list of selection criteria
    coordinated_phrase = nlg_factory.createCoordinatedPhrase()
    for modifier in modifiers:
        coordinated_phrase.addCoordinate(modifier)

    # Here's where we assemble the subject (the elements getting selected)
    # and the criteria into a coherent whole:
    clause.addComplement(coordinated_phrase)

    # As a last step, if what's getting chosen is actually a pseudo-element
    # then we swap that out as the subject of the sentence.
    if pseudoelement_phrase is not None:
        elements_phrase = clause
        clause = pseudoelement_phrase
        preposition = nlg_factory.createPrepositionPhrase()
        preposition.addComplement(elements_phrase)
        preposition.setPreposition('for')
        clause.addComplement(preposition)

    return clause


def explain_selector(selector):

    phrase = None

    for index, child in enumerate(selector.getChildren()):

        # If this is a simple selector sequence, explain what is choosing.
        # Add prepositions that describe how the combinator relates this sequence
        # to the last visited sequence.
        if isinstance(child, CssParser.Simple_selector_sequenceContext):
            focus = (index == len(selector.children) - 1)  # it's in focus if it's the last one.
            simple_selector_sequence_phrase =\
                explain_simple_selector_sequence(child, focus)
            if phrase is not None:
                simple_selector_sequence_phrase.addComplement(phrase)
            phrase = simple_selector_sequence_phrase

        # If this is a combinator, form a preposition that will link the next
        # encountered sequence to the last one by describing the relationship
        # between the two sequences.
        elif isinstance(child, CssParser.CombinatorContext):

            # Get the name of the symbol that defines this combinator
            combinator_symbol = child.children[0].symbol.type

            # A space is just selecting one sequence "from" another
            if combinator_symbol == CssLexer.SPACE:
                preposition = nlg_factory.createPrepositionPhrase('from')
                preposition.addComplement(phrase)
                phrase = preposition

            # A greater-than sign tells us that a later sequence chooses
            # "children of" a later sequence.
            elif combinator_symbol == CssLexer.GREATER:

                complement = nlg_factory.createClause()
                complement.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)

                verb = nlg_factory.createVerbPhrase('be')
                complement.setVerb(verb)

                object_ = nlg_factory.createNounPhrase('child')
                object_.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
                complement.setObject(object_)

                # Here's where we connect this sequence to the past one,
                # through and 'of' preposition.
                preposition = nlg_factory.createPrepositionPhrase('of')
                preposition.addComplement(phrase)
                object_.addComplement(preposition)
                phrase = complement

            # A tilde sign tells us that a later sequence chooses elements that
            # are siblings of and eventually appear after those specified
            # by an earlier sequence.
            elif combinator_symbol == CssLexer.TILDE:

                complement = nlg_factory.createCoordinatedPhrase()
                complement.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)

                siblings_clause = nlg_factory.createClause()
                verb = nlg_factory.createVerbPhrase('be')
                siblings_clause.setVerb(verb)
                object_ = nlg_factory.createNounPhrase('sibling')
                object_.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
                siblings_clause.setObject(object_)
                preposition = nlg_factory.createPrepositionPhrase('of')
                object_.addComplement(preposition)
                complement.addCoordinate(siblings_clause)

                appearance_clause = nlg_factory.createClause()
                verb = nlg_factory.createVerbPhrase('appear')
                verb.addPreModifier('eventually')
                appearance_clause.setVerb(verb)
                preposition = nlg_factory.createPrepositionPhrase('after')
                preposition.addComplement(phrase)
                verb.addComplement(preposition)
                complement.addCoordinate(appearance_clause)

                phrase = complement

            # The plus symbol is used when the elements specified by a second sequence
            # are siblings of and appear right after the elements specified by a first sequence.
            # The construction here is practically the same as that for the ~ symbol,
            # as it uses almost the same phrasing to describe the relationship.
            elif combinator_symbol == CssLexer.PLUS:

                "are siblings of and appear right after elements"
                complement = nlg_factory.createCoordinatedPhrase()
                complement.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)

                siblings_clause = nlg_factory.createClause()
                verb = nlg_factory.createVerbPhrase('be')
                siblings_clause.setVerb(verb)
                object_ = nlg_factory.createNounPhrase('sibling')
                object_.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
                siblings_clause.setObject(object_)
                preposition = nlg_factory.createPrepositionPhrase('of')
                object_.addComplement(preposition)
                complement.addCoordinate(siblings_clause)

                appearance_clause = nlg_factory.createClause()
                verb = nlg_factory.createVerbPhrase('appear')
                appearance_clause.setVerb(verb)
                preposition = nlg_factory.createPrepositionPhrase('after')
                preposition.addPreModifier('right')
                preposition.addComplement(phrase)
                verb.addComplement(preposition)
                complement.addCoordinate(appearance_clause)

                phrase = complement

    return phrase


def explain_selectors_group(selectors_group):

    # If there is more than one selector in a list, just explain each of them.
    # Add them to a dictionary that's indexed by the selector text.
    clauses = {}
    for selector in selectors_group.getTypedRuleContexts(CssParser.SelectorContext):
        clause = explain_selector(selector)
        selector_text = selector.getText()
        clauses[selector_text] = clause

    return clauses


class CssExplainer(CssListener, ErrorListener):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def exitSelectors_group(self, context):
        self.result = explain_selectors_group(context)
