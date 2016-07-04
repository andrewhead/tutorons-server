#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from antlr4.error.ErrorListener import ErrorListener
from bs4 import BeautifulSoup
import re
from antlr4.tree.Tree import TerminalNodeImpl as TerminalNode
# We use PyQuery here for constructing an HTML document as it replicates a lot
# of the jQuery API.  I expect that most people who will maintain or change this
# file will have some knowledge of jQuery, so this is intended to make this
# document easier to read and maintain.
from pyquery import PyQuery as P

from parsers.common.util import parse_plaintext, walk_tree
from parsers.css.CssLexer import CssLexer
from parsers.css.CssParser import CssParser
from parsers.css.CssListener import CssListener


logging.basicConfig(level=logging.INFO, format="%(message)s")
# The following is the type of tag that all selected elements will have if their
# tag hasn't been specified explicitly in the selector
UNSPECIFIED_ELEMENT_TAG = 'div'


'''
There are a few different types of methods for our example generation.
Example generation creates an HTML document with a node selected by the selector.
The grammar rules we have here each do one of the following:
* generate an HTML node
* decorate a node (for example, with a class, ID, or attribute)
* place a node relative to another node (as a child, descendant, or sibling)
'''


def generate_examples(selector, indent=4):
    example_generator = CssExampleGenerator()
    renderer = HtmlRenderer()
    try:
        parse_tree = parse_plaintext(selector, CssLexer, CssParser, 'selectors_group')
        walk_tree(parse_tree, example_generator)
        examples = {}
        for selector, contents in example_generator.result.items():
            examples[selector] = renderer.render_html_contents(contents, indent_level=indent)
        return examples
    except Exception as exception:
        # Although this is a pretty broad catch, we want the default
        # behavior of example generation to be that the program continues to
        # run, even if one selector was not properly explained.
        logging.error("Error generating examples: %s", str(exception))
        return None


def annotate_attribute(element, attribute_node):

    EQUALITY_SYMBOLS = [
        CssLexer.PREFIXMATCH,
        CssLexer.SUFFIXMATCH,
        CssLexer.SUBSTRINGMATCH,
        CssLexer.EQUALS,
        CssLexer.INCLUDES,
        CssLexer.DASHMATCH,
    ]

    state = 'seeking attribute'
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
            value = child.getText().strip('"').strip("'")
            state = 'found all'

    if equality_operation == CssLexer.PREFIXMATCH:
        element.attr(attribute_name, value + "_suffix")
    elif equality_operation == CssLexer.SUFFIXMATCH:
        element.attr(attribute_name, 'prefix_' + value)
    elif equality_operation == CssLexer.SUBSTRINGMATCH:
        element.attr(attribute_name, 'prefix_' + value + '_suffix')
    elif equality_operation == CssLexer.EQUALS:
        element.attr(attribute_name, value)
    elif equality_operation == CssLexer.INCLUDES:
        element.attr(attribute_name, 'value1 ' + value + ' value2')
    elif equality_operation == CssLexer.DASHMATCH:
        element.attr(attribute_name, value + '-suffix')

    return element


def annotate_hash(element, hash_node):
    id_ = hash_node.getText().lstrip('#')
    element.attr('id', id_)
    return element


def annotate_class(element, class_node):
    class_name = class_node.children[1].getText()
    element.addClass(class_name)
    return element


def annotate_pseudoclass(element, pseudo_node):

    PSEUDOCLASS_DESCRIPTIONS = {
        'checked': "This input has been 'checked'",
        'visible': "This element is 'visible' (it contains space in the document)",
        'hidden': "This element is 'hidden' (it is of type hidden, consumes no space, or " +
                  "has 'display' property set to 'none'",
        'enabled': "This element is 'enabled' to accept input or focus",
        'active': "This element is being clicked by the mouse",
        'empty': "This element has no children",
        'visited': "This user has visited this link before",
    }

    functionalPseudo = pseudo_node.getChild(0, CssParser.Functional_pseudoContext)
    if functionalPseudo is not None:
        # Here's where we need to make a bunch of custom rules for different
        # functional pseudo-classes, as each of them have some pretty involved
        # behavior that's not very easy to demonstrate with simple comments.
        # For now we settle with a pretty simple and very vague default.
        description =\
            "This element satisfies the functional pseudoclass '" +\
            functionalPseudo.getText() + "'"
    else:
        pseudoclass = pseudo_node.children[1].getText()
        description = PSEUDOCLASS_DESCRIPTIONS.get(
            pseudoclass,
            "This element has the pseudoclass '" + pseudoclass + "'"
        )

    # If this is an input element (which cannot have any children), then we add
    # this note as an attribute.
    if re.match('<input', str(element)):
        element.attr("tip", description)
    else:
        element.append("<!--This element " + description + "-->")
    return element


def append_pseudoelement(element, pseudo_node):

    # Check to see if this pseudoelement is a functional pseudo-element.
    # If it is, and we succeed at generating example behavior for it as a functional
    # pseudo-element, then use this augmentation.
    # Otherwise, proceed to explain it as a generic pseudo-element
    # (See the note in the functional pseudo-element routine about how functional
    # pseudo-elements don't exist in the actual selectors spec).
    if isinstance(pseudo_node.children[2], CssParser.Functional_pseudoContext):
        selection = annotate_functional_pseudoelement(element, pseudo_node)
        if selection is not None:
            return selection

    pseudoelement_name = pseudo_node.children[2].getText()

    if pseudoelement_name == 'first-letter':
        element.append(
            "<mark>The selector chooses the first letter of text in this element</mark>"
        )
        selection = element
    elif pseudoelement_name == 'first-line':
        element.append(
            "<mark>The first line of content displayed for this element gets chosen</mark>\n" +
            "but the second line doesn't."
        )
        selection = element
    elif pseudoelement_name == 'before':
        selection = P([
            "<mark>This content (generated before a specific element) will be selected</mark>",
            element,
        ])
    elif pseudoelement_name == 'after':
        selection = P([
            element,
            "<mark>This content (generated before a specific element) will be selected</mark>",
        ])
    elif pseudoelement_name == 'text':
        element.append(
            "<mark>The text content of this element will be selected</mark>"
        )
        selection = element
    else:
        element.append(
            "<mark><!--The selector chooses content from the '" + pseudoelement_name +
            "' pseudo-element of this element--></mark>"
        )
        selection = element

    return selection


def annotate_functional_pseudoelement(element, pseudo_node):
    '''
    Annotate an HTML node with attributes and comments demonstrating what is getting chosen
    by a functional pseudo-element.
    This method returns None if it can't find a specialized explanation for this pseudoelement.
    This allows whatever calls it to make a more generic explanation if this method fails.

    Note that functional pseudo-elements don't exist in the vurrent celectors specification:
    https://www.w3.org/TR/css3-selectors/#pseudo-elements
    However, functional pseudo-elements are supported by some web scraping libraries, for example
    the '::attr(<attr_name>)' pseudo-element for Scrapy:
    http://doc.scrapy.org/en/latest/topics/selectors.html
    This function provides support for making examples of what these unofficial selectors do.
    '''
    # Extract name of function and expression from parse tree
    # Function tokens for pseudo-elements are grouped with a right parenthesis, which we remove
    functional_pseudo_node = pseudo_node.children[2]
    function_token = functional_pseudo_node.children[0].getText()
    function_name = re.sub('\($', '', function_token)
    expression_node = functional_pseudo_node.getTypedRuleContexts(CssParser.ExpressionContext)[0]
    expression = expression_node.getText()

    if function_name == 'attr':

        # Only provide a "placeholder" value of the attribute if it isn't already specified
        # by some other selector (for instance, by an attribute simple selector).
        if element.attr(expression) is None:
            element.attr(expression, "<This value is selected>")

        # Add a (highlighted) comment explaining that the attribute is getting selected.
        element.append(
            "<mark><!--The selector chooses the value of this element's '" +
            expression + "' attribute--></mark>",
        )
        return element

    return None


def annotate_pseudo(element, pseudo_node):
    '''
    Returns tuple: (content generated, whether a pseudo-element was created)
    '''
    colon_count = 0
    for child in pseudo_node.children:
        if isinstance(child, TerminalNode) and child.symbol.type == CssLexer.COLON:
            colon_count += 1
            if colon_count >= 2:
                break

    pseudo_type = 'class' if colon_count == 1 else 'element'
    if pseudo_type == 'class':
        return annotate_pseudoclass(element, pseudo_node), False
    elif pseudo_type == 'element':
        return append_pseudoelement(element, pseudo_node), True


def _create_element_with_tag(tag_name, namespace=None):

    # Create a verbose tag name with an optional namespace
    namespaced_tag_name = namespace + ':' + tag_name if namespace is not None else tag_name

    # Construct HTML for the open and close of the tag.
    # If there's a namespace for the tag, we need to make sure that there's some
    # attribute pointing the XML parser to the site where the namespace is defined.
    # For the time being, we add that attribute to the element itself (though I
    # expect this is very unlikely to happen in practice).
    html = "<" + namespaced_tag_name
    if namespace is not None:
        html += ' xmlns:' + namespace + "=\"https://namespace-site.com\""
    html += "></" + namespaced_tag_name + ">"

    # One way to support a namespaced tag is to parse it with the 'xml' parser.
    # I don't know if this trick is the only way, but I found out that we could
    # do this by looking through the test code for PyQuery at:
    # https://github.com/gawel/pyquery/blob/master/tests/test_pyquery.py
    return P(html, parser='xml')


def _get_namespace(element_selector_node):
    '''
    Given the similarity between the production rules for the type selector
    and for the universal selector, we provide a single routine that will
    extract the namespace for either.
    This returns the string of the namespace name if there is one, and `None` otherwise.
    '''
    namespace_prefix = element_selector_node.getChild(0, CssParser.Namespace_prefixContext)
    if namespace_prefix is not None:
        namespace_identifier = namespace_prefix.children[0]
        if namespace_identifier.symbol.type == CssLexer.IDENTIFIER:
            return namespace_identifier.getText()
    return None


def create_element_from_universal(universal_node):
    namespace = _get_namespace(universal_node)
    element_name = UNSPECIFIED_ELEMENT_TAG
    return _create_element_with_tag(element_name, namespace)


def create_element_from_type_selector(type_selector_node):
    namespace = _get_namespace(type_selector_node)
    element_name = type_selector_node.getChild(0, CssParser.Element_nameContext).getText()
    return _create_element_with_tag(element_name, namespace)


def create_content_from_simple_selector_sequence(simple_selector_sequence_node, focus):
    '''
    Note that this method can return more than just an HTML element.
    It returns a selection with HTML content that may include multiple
    nodes.  An example of where this might happen is if content is generated
    that can match a `::before` pseudo-element.
    '''
    tag_determiner = simple_selector_sequence_node.children[0]
    if isinstance(tag_determiner, CssParser.Type_selectorContext):
        element = create_element_from_type_selector(tag_determiner)
    elif isinstance(tag_determiner, CssParser.UniversalContext):
        element = create_element_from_universal(tag_determiner)
    content = element

    # Each selector in the sequence produces another layer of specificity.
    # In this loop, we apply annotations for each selector to the element we've created.
    # so that we can append them into a joined list at the end to describe
    # the entire sequence.
    pseudo_mark_added = False
    for selector in simple_selector_sequence_node.children[1:]:
        if isinstance(selector, CssParser.PseudoContext):
            content, mark_added = annotate_pseudo(content, selector)
            # Save whether a "mark" has been made that the selection is being made
            # on a pseudo-element.  If it is, then we need to remember this
            # to see whether we should mark the main element
            pseudo_mark_added = mark_added or pseudo_mark_added
        elif isinstance(selector, CssParser.AttributeContext):
            content = annotate_attribute(content, selector)
        elif isinstance(selector, CssParser.Class_Context):
            content = annotate_class(content, selector)
        elif isinstance(selector, CssParser.Hash_Context):
            content = annotate_hash(content, selector)

    # Mark up the main contents if a pseudo-element hasn't been added and this
    # particular selector sequence is the focus
    if focus is True and pseudo_mark_added is False:
        content = content.wrapAll('<mark></mark>')

    return content


def create_content_from_selector(selector_node):

    root = None
    last_content = None
    last_combinator = None

    for index, child in enumerate(selector_node.getChildren()):

        # If this is a simple selector sequence, create a node of what it is choosing.
        if isinstance(child, CssParser.Simple_selector_sequenceContext):

            focus = (index == len(selector_node.children) - 1)  # it's in focus if it's the last one

            # Create HTML content from this simple selector sequence
            content = create_content_from_simple_selector_sequence(child, focus)

            # The root of the selection is going to be the very first content created
            if root is None:
                root = content

            # If a combinator has been defined, then there is a link between the recently created
            # content and the last content created.
            if last_combinator is not None and last_content is not None:

                # Get the name of the symbol that defines this combinator
                combinator_symbol = last_combinator.children[0].symbol.type

                # Child combinator
                if combinator_symbol == CssLexer.GREATER:
                    last_content.append(content)

                # Descendant combinator
                elif combinator_symbol == CssLexer.SPACE:
                    descendant = content
                    child = _create_element_with_tag(UNSPECIFIED_ELEMENT_TAG)
                    child.append(descendant)
                    last_content.append(child)

                # Generalized sibling combinator
                elif combinator_symbol == CssLexer.TILDE:

                    # First, create a sibling that's NOT supposed to match
                    siblings = _create_element_with_tag(UNSPECIFIED_ELEMENT_TAG)

                    # Then, add the content that's supposed to match right after it
                    siblings.extend(content)

                    # Finally, add both of the siblings (unmatching and matching) after
                    # the last content generated.
                    last_content.extend(siblings)

                # Next sibling combinator
                elif combinator_symbol == CssLexer.PLUS:
                    last_content.extend(content)

            # Save a link to the content so that it can be referenced when attaching
            # other content described by the selector to this content
            last_content = content

        # If this is a combinator, hold onto it so we can know how the next generated
        # content should be attached to previously generated content.
        elif isinstance(child, CssParser.CombinatorContext):
            last_combinator = child

    return root


def create_content_from_selectors_group(selectors_group_node):

    contents = {}
    for selector in selectors_group_node.getTypedRuleContexts(CssParser.SelectorContext):
        html_contents = create_content_from_selector(selector)
        selector_text = selector.getText()
        contents[selector_text] = html_contents

    return contents


class HtmlRenderer(object):

    def render_html_contents(self, contents, indent_level=2):
        '''
        Input is provided as PyQuery object consisting of one or several HTML
        nodes that need to be rendered.  Everything that is surrounded with a
        <mark></mark> tag will instead get surrounded with a
        <span class='tutorons_selection'></span> span.
        The result is a pretty string.
        '''
        # Join the contents into a single chunk of HTML
        html = '\n'.join([P(element).outer_html() for element in contents])

        # BeautifulSoup has a built-in prettifier that will get us most
        # of the way to a presentable document
        # We choose the 'html.parser' instead of the 'html5lib' parser because
        # 1. We should be providing it valid HTML documents (no big need for leniency)
        # 2. The documents are also small, so performance isn't that important right now.
        # 3. 'html5lib' adds unwanted tags to make a document into valid HTML.
        #    We're only interested in showing HTML fragments, not full documents.
        soup_document = BeautifulSoup(html, 'html.parser')
        prettified_text = soup_document.prettify()

        # Apply a number of transformations to escape and indent the
        # text to prepare it for presentation
        stripped_text = prettified_text.strip()
        escaped_text = self._escape(stripped_text)
        marked_text = self._format_marked_content(escaped_text)
        spans_unindented_text = self._unindent_spans(marked_text)
        indented_text = self._indent(spans_unindented_text, indent_level)
        return indented_text

    def _indent(self, text, indent_level):

        lines = text.split('\n')
        for index, line in enumerate(lines):

            # Detect the spaces at the start of each line, and the text that comes after it.
            spaces, line_text = re.match('^( *)([^ ].*)', line).groups()

            # Do nothing if this line only contains a span (I can't remember why, but
            # it's probably because this is used for formatting only and won't be seen.
            if re.match(r" *</?span", line):
                line = line_text
            # Otherwise, reset the number of spaces at the start of the line based
            # on the number of spaces that were there before, multiplied by the indent level.
            else:
                new_spaces_count = len(spaces) * indent_level
                escaped_spaces = new_spaces_count * '&nbsp;'
                line = escaped_spaces + line_text + "<br>"

            lines[index] = line

        return '\n'.join(lines)

    def _format_marked_content(self, text):
        '''
        Surround any marked content with a span that can be formatted on the page.
        '''
        left_mark_replaced = re.sub(r"<mark>", "<span class='tutoron_selection'>", text)
        marks_replaced = re.sub(r"</mark>", "</span>", left_mark_replaced)
        return marks_replaced

    def _escape(self, text):
        '''
        Escaped characters that have a special meaning in HTML to make sure
        that they render as the right character from within a code block.
        '''
        # When we escape ampersands, we avoid those that are already part of escaped chevrons.
        ampersands_escaped = re.sub(r"&(?!(lt;|gt;))", "&amp;", text)
        # When we escape the '<' and '>' characters, we make sure to avoid those that
        # are attached to a 'mark' tag, as these need to be preserved to make sure that
        # we can substitute them with a span with class "tutoron_selection"
        left_bracket_escaped = re.sub(r"<(?!/?mark)", "&lt;", ampersands_escaped)
        right_bracket_escaped = re.sub(r"(?<!mark)>", "&gt;", left_bracket_escaped)
        all_escaped = right_bracket_escaped
        return all_escaped

    def _unindent_spans(self, text):
        '''
        We want to make sure that after we have inserted our new spans for
        marked content that we remove any indentations that came from them
        being seen as elements to begin with.  This routine removes that indentation.
        It also (I think) assumes that the only spans in the HTML tree are ones
        that we have added to mark chosen content.
        '''
        span_level = 0
        lines = text.split('\n')

        for index, line in enumerate(lines):

            # Watch for the end of a span
            if re.match(" *</span", line):
                span_level -= 1

            # Remove one space for every level of span
            new_line = re.sub('^' + ' ' * span_level, '', line)
            lines[index] = new_line

            # Watch for the start of a span
            if re.match(" *<span", line):
                span_level += 1

        return '\n'.join(lines)


class CssExampleGenerator(CssListener, ErrorListener):
    ''' Generates PyQuery HTML documents that satisfy a selector. '''

    def exitSelectors_group(self, context):
        self.result = create_content_from_selectors_group(context)
