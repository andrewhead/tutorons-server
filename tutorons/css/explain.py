#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.InputStream import InputStream
from antlr4.error.ErrorListener import ErrorListener

from tutorons.common.java.simplenlg import factory as nlg_factory,\
    realiser, Feature, NumberAgreement
from parsers.css.CssLexer import CssLexer
from parsers.css.CssParser import CssParser
from parsers.css.CssListener import CssListener


logging.basicConfig(level=logging.INFO, format="%(message)s")


def explain(selector):
    walker = ParseTreeWalker()
    explainer = CssExplainer()
    input = InputStream(selector)
    lexer = CssLexer(input)
    stream = CommonTokenStream(lexer)
    parser = CssParser(stream)
    tree = parser.selector()
    try:
        walker.walk(explainer, tree)
    except Exception as e:
        logging.error("Encountered exception explaining CSS: %s", str(e))
    return explainer.result


# Convenience function for getting the unique identifier of a node that the
# walker is currently visiting that can be used to hash results
_key = lambda ctx: ctx.invokingState


class CssExplainer(CssListener, ErrorListener):
    '''
    Generates English explanations of what a CSS selector chooses.
    Ported from the Java code that we made for the same purpose.
    '''
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.phrases = {}

    def exitSelector(self, ctx):
        sentence = nlg_factory.createClause()
        noun = nlg_factory.createNounPhrase('selector')
        noun.setDeterminer('the')
        noun.addPostModifier("'" + ctx.getText() + "'")
        sentence.setSubject(noun)
        sentence.setVerb('chooses')
        sentence.setComplement(self.phrases[_key(ctx.node())])
        self.result = realiser.realiseSentence(sentence)

    def syntaxError(self, *args, **kwargs):
        print "Syntax Error!"

    def _getTagNoun(self, tag):
        EXPANSIONS = {
            'p': 'paragraph',
            'div': 'container',
            'strong': 'bolded text',
            'a': 'link',
            'img': 'image',
            'pre': 'preformatted text',
            'table': 'table',
            'tr': 'row',
            'td': 'cell',
        }
        if tag == 'h3':
            noun = nlg_factory.createNounPhrase('header')
            noun.addPostModifier('(of level 3)')
            return noun
        else:
            noun_text = EXPANSIONS.get(tag, tag)
            return nlg_factory.createNounPhrase(noun_text)

    def _getPseudoclassAdjective(self, pseudoclass):
        adjectival_pseudoclasses = [
            'checked',
            'hidden',
            'visible',
            'enabled',
            'active',
            'empty',
            'visited',
        ]
        if pseudoclass in adjectival_pseudoclasses:
            return pseudoclass
        if pseudoclass == 'hover':
            return 'hovered-over'
        if pseudoclass == 'focus':
            return 'in-focus'
        return None

    def exitNode(self, ctx):

        if ctx.element() is not None:
            tag = ctx.element().IDENT().getText()
            tag_noun = self._getTagNoun(tag)
        else:
            tag_noun = nlg_factory.createNounPhrase('element')

        # Describe classes and IDs (pluralizing as we go if need be)
        if ctx.qualifier() is not None:
            qualifier = ctx.qualifier()
            if qualifier.ident() is not None:
                tag_noun.setFeature(Feature.NUMBER, NumberAgreement.SINGULAR)
                tag_noun.setDeterminer('a')
                tag_noun.addPostModifier(
                    "with the ID '" + qualifier.ident().IDENT().getText() + "'"
                )
            elif qualifier.klazz() is not None:
                tag_noun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
                tag_noun.addPostModifier(
                    "of class '" + qualifier.klazz().IDENT().getText() + "'"
                )
        else:
            tag_noun.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)

        if ctx.pseudoclass() is not None:
            pseudoclass = ctx.pseudoclass().IDENT().getText()
            adjective = self._getPseudoclassAdjective(pseudoclass)
            if adjective is not None:
                tag_noun.addPreModifier(adjective)
            else:
                generic_modifier = ''
                if ctx.qualifier() is not None:
                    generic_modifier = 'and '
                else:
                    generic_modifier = 'with '
                generic_modifier += ('pseudoclass ' + pseudoclass)
                tag_noun.addPostModifier(generic_modifier)

        # Decide whether we describe the element or its property as
        # the subject of this clause
        if not ctx.prop():
            node_noun = tag_noun
        else:
            property_ = ctx.prop().IDENT().getText()
            node_noun = self._getPropertyNoun(property_)
            node_noun.addPostModifier('from')
            node_noun.addPostModifier(tag_noun)

        if ctx.attr() is not None:
            node_noun.addPostModifier('with')
            attribute_phrase = self.phrases[_key(ctx.attr())]
            if node_noun.getFeature(Feature.NUMBER) == NumberAgreement.PLURAL:
                attribute_phrase.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
            node_noun.addPostModifier(attribute_phrase)

        if ctx.node() is not None:
            child_phrase = self.phrases[_key(ctx.node())]
            child_phrase.addPostModifier('from')
            child_phrase.addPostModifier(node_noun)
            self.phrases[_key(ctx)] = child_phrase
        else:
            self.phrases[_key(ctx)] = node_noun

    def exitAttr(self, ctx):
        noun = nlg_factory.createNounPhrase()
        if ctx.attrname().getText() == 'href':
            noun.setNoun('URL')
        else:
            noun.setNoun(ctx.attrname().getText())

        if ctx.rel().getText() == '^=':
            noun.addPostModifier('starting with')
        else:
            noun.addPostModifier('related to')

        noun.addPostModifier("'" + ctx.attrvalue().getText + "'")
        self.phrases(ctx, noun)
