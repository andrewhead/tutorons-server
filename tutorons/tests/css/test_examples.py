#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
from pyquery import PyQuery as P
import re

from parsers.css.CssLexer import CssLexer
from parsers.css.CssParser import CssParser
from parsers.common.util import parse_plaintext
from tutorons.css.examples import annotate_attribute, annotate_hash, annotate_class,\
    annotate_pseudo, create_element_from_universal, create_element_from_type_selector,\
    create_content_from_simple_selector_sequence, create_content_from_selector,\
    create_content_from_selectors_group, HtmlRenderer


logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_selector(selector, rule_name):
    '''
    The selector here can be partial.  And this method returns partial
    parse results: it can be parsed as just a specific rule from the
    grammar, as specified by `rule_name`.
    '''
    return parse_plaintext(selector, CssLexer, CssParser, rule_name)


def _get_comment_children(node):
    comment_children = []
    for child in node.children():
        if re.match("^<!--.*-->$", str(child)):
            comment_children.append(child)
    return comment_children


def _element_has_tag(element, tag):
    ''' Element needs to be passed in as a PyQuery selection. '''
    return bool(re.match("<" + tag + ".+</" + tag + ">", element.outer_html()))


class AttributeAnnotationTest(unittest.TestCase):

    def test_annotate_node_with_attribute(self):
        attribute = parse_selector('[href="http://url.com"]', 'attribute')
        node = P('<div></div>')
        node = annotate_attribute(node, attribute)
        self.assertEqual(node.attr('href'), "http://url.com")

    def test_annotate_node_with_attribute_that_starts_with_value(self):
        attribute = parse_selector('[href^="http://url.com"]', 'attribute')
        node = P('<div></div>')
        node = annotate_attribute(node, attribute)
        self.assertGreater(len(node.attr('href')), 14)
        self.assertTrue(node.attr('href').startswith("http://url.com"))

    def test_annotate_node_with_attribute_that_ends_with_value(self):
        attribute = parse_selector('[href$="url.com"]', 'attribute')
        node = P('<div></div>')
        node = annotate_attribute(node, attribute)
        self.assertGreater(len(node.attr('href')), 7)
        self.assertTrue(node.attr('href').endswith("url.com"))

    def test_annotate_node_with_attribute_with_substring(self):
        attribute = parse_selector('[href*="url.com"]', 'attribute')
        node = P('<div></div>')
        node = annotate_attribute(node, attribute)
        self.assertGreater(len(node.attr('href')), 7)
        self.assertTrue("url.com" in node.attr('href'))
        self.assertFalse(
            node.attr('href').endswith("url.com") or
            node.attr('href').startswith("url.com")
        )

    def test_annotate_node_with_attribute_including_value(self):
        attribute = parse_selector('[href~="url.com"]', 'attribute')
        node = P('<div></div>')
        node = annotate_attribute(node, attribute)
        self.assertGreater(len(node.attr('href')), 7)
        self.assertTrue(re.search(r"(^|\b)url\.com(\b|$)", node.attr('href')))

    def test_annotate_node_with_attribute_matching_dash_value(self):
        # This scenario is taken from the example in the W3C selectors documentation:
        # https://www.w3.org/TR/css3-selectors/#attribute-representation
        # Usually, a 'dash match' is used for language subcodes.
        attribute = parse_selector('[href|="en"]', 'attribute')
        node = P('<div></div>')
        node = annotate_attribute(node, attribute)
        self.assertGreater(len(node.attr('href')), 2)
        self.assertTrue(node.attr('href').startswith('en'))


class HashAnnotationTest(unittest.TestCase):

    def test_annotate_node_with_hash(self):
        hash_ = parse_selector('#my_id', 'hash_')
        node = P('<div></div>')
        node = annotate_hash(node, hash_)
        self.assertEqual(node.attr('id'), 'my_id')


class ClassAnnotationTest(unittest.TestCase):

    def test_annotate_node_with_class(self):
        class_ = parse_selector('.klazz', 'class_')
        node = P('<div></div>')
        node = annotate_class(node, class_)
        self.assertEqual(node.attr('class'), 'klazz')


class PseudoclassCommentTest(unittest.TestCase):

    def test_add_custom_comment_to_node_about_pseudoclass(self):
        pseudo = parse_selector(':checked', 'pseudo')
        node = P('<div></div>')
        node, _ = annotate_pseudo(node, pseudo)
        comment_children = _get_comment_children(node)
        self.assertEqual(len(comment_children), 1)
        self.assertIn("This input has been 'checked'", comment_children[0].text)

    def test_add_generic_comment_to_node_about_unknown_pseudoclass(self):
        pseudo = parse_selector(':unknown', 'pseudo')
        node = P('<div></div>')
        node, _ = annotate_pseudo(node, pseudo)
        comment_children = _get_comment_children(node)
        self.assertEqual(len(comment_children), 1)
        self.assertIn("This element has the pseudoclass 'unknown'", comment_children[0].text)


class PseudofunctionCommentTest(unittest.TestCase):

    def test_add_generic_comment_to_node_about_unknown_functional_pseudoclass(self):
        pseudo = parse_selector(':unknown-function(parameter)', 'pseudo')
        node = P('<div></div>')
        node, _ = annotate_pseudo(node, pseudo)
        comment_children = _get_comment_children(node)
        self.assertEqual(len(comment_children), 1)
        self.assertIn(
            "This element satisfies the functional pseudoclass 'unknown-function(parameter)'",
            comment_children[0].text
        )


class PseudoelementAppendTest(unittest.TestCase):

    def test_highlight_first_line_of_first_letter_pseudoelement(self):
        pseudo = parse_selector('::first-letter', 'pseudo')
        node = P('<div></div>')
        node, _ = annotate_pseudo(node, pseudo)
        self.assertTrue(re.match('<mark>[^\n]+</mark>', node.html()))

    def test_highlight_first_line_for_first_line_pseudoelement(self):
        pseudo = parse_selector('::first-line', 'pseudo')
        node = P('<div></div>')
        node, _ = annotate_pseudo(node, pseudo)
        # Text should have been produced that includes:
        # A line at least one character in length that is highlighted
        # Another line at least one character in length that isn't highlighted
        self.assertTrue(re.match('<mark>.+</mark>\n.', node.html(), flags=re.MULTILINE))

    def test_generate_content_before_element_for_before_pseudoelement(self):

        pseudo = parse_selector('::before', 'pseudo')
        node = P('<div></div>')
        nodes, _ = annotate_pseudo(node, pseudo)

        # The function for annotation is now going to return a selection with both
        # the original node, and a new node that comes right before it.  This
        # is in contrast to the other functions, which just modify the node passed in.
        self.assertEqual(nodes.length, 2)
        self.assertTrue(_element_has_tag(P(nodes[0]), 'mark'))
        self.assertEqual(P(nodes[1]), node)

    def test_generate_content_after_element_for_after_pseudoelement(self):
        pseudo = parse_selector('::after', 'pseudo')
        node = P('<div></div>')
        nodes, _ = annotate_pseudo(node, pseudo)
        self.assertEqual(nodes.length, 2)
        self.assertEqual(P(nodes[0]), node)
        self.assertTrue(_element_has_tag(P(nodes[1]), 'mark'))


class UniversalSelectorElementCreationTest(unittest.TestCase):

    def test_create_div_element_for_universal_selector(self):
        universal = parse_selector('*', 'universal')
        element = create_element_from_universal(universal)
        self.assertTrue(_element_has_tag(element, 'div'))

    def test_create_div_element_with_specified_namespace(self):
        universal = parse_selector('namespace|*', 'universal')
        element = create_element_from_universal(universal)
        self.assertTrue(_element_has_tag(element, 'namespace|div'))

    def test_ignore_universal_namespace(self):
        universal = parse_selector('*|*', 'universal')
        element = create_element_from_universal(universal)
        self.assertTrue(_element_has_tag(element, 'div'))


class TypeSelectorElementCreationTest(unittest.TestCase):

    def test_create_element_with_same_tag_as_type_selector(self):
        type_selector = parse_selector('html', 'type_selector')
        element = create_element_from_type_selector(type_selector)
        self.assertTrue(_element_has_tag(element, 'html'))

    def test_element_tag_includes_namespace_if_specified(self):
        type_selector = parse_selector('namespace|html', 'type_selector')
        element = create_element_from_type_selector(type_selector)
        self.assertTrue(_element_has_tag(element, 'namespace:html'))


class SimpleSelectorSequenceElementCreationTest(unittest.TestCase):

    def test_create_element_matching_multiple_selectors_with_conjunction(self):
        sequence = parse_selector('p.klazz[href^=\'http://\']', 'simple_selector_sequence')
        element = create_content_from_simple_selector_sequence(sequence, False)
        self.assertEqual(element.length, 1)
        self.assertTrue(_element_has_tag(element, 'p'))
        self.assertIn('klazz', element.attr('class'))
        self.assertTrue(element.attr('href').startswith("http://"))

    def test_create_div_if_element_unspecified(self):
        sequence = parse_selector('.klazz', 'simple_selector_sequence')
        element = create_content_from_simple_selector_sequence(sequence, False)
        self.assertTrue(_element_has_tag(element, 'div'))
        self.assertIn('klazz', element.attr('class'))

    def test_mark_main_element_if_the_element_has_focus(self):
        sequence = parse_selector('.klazz', 'simple_selector_sequence')
        element = create_content_from_simple_selector_sequence(sequence, focus=True)
        self.assertTrue(_element_has_tag(element, 'mark'))
        self.assertEqual(element('div.klazz').length, 1)

    def test_dont_mark_main_element_if_element_has_focus_and_pseudoelement(self):
        sequence = parse_selector('.klazz::first-line', 'simple_selector_sequence')
        element = create_content_from_simple_selector_sequence(sequence, focus=True)
        self.assertFalse(_element_has_tag(element, 'mark'))


class SelectorContentCreationTest(unittest.TestCase):

    def test_append_children_to_parents(self):

        selector = parse_selector('.klazz > p', 'selector')
        element = create_content_from_selector(selector)
        self.assertEqual(element.attr('class'), 'klazz')

        # The main element's one and only child should be the paragraph
        self.assertEqual(element.children().length, 1)
        self.assertTrue(_element_has_tag(P(element.children()[0]), 'mark'))

    def test_append_descendants_to_multiple_levels_of_depth(self):

        selector = parse_selector('.klazz p', 'selector')
        element = create_content_from_selector(selector)

        # The condition for readers to be able to visually differentiate between
        # a descendant and a child should be, I think, that a descendant will
        # be more than one level deeper than the parent.  So, with the next
        # selector, we check to make sure that the 'p' element is nested
        # at a level deeper than the immediate children.
        self.assertGreater(element.children('* p').length, 0)

    def test_add_next_sibling_after_selected_sequence(self):

        selector = parse_selector('.klazz + p', 'selector')
        elements = create_content_from_selector(selector)

        # The sibling should be the element right after the element to the left of the combinator
        self.assertEqual(P(elements[0]).attr('class'), 'klazz')
        self.assertTrue(_element_has_tag(P(elements[1]), 'mark'))
        self.assertTrue(_element_has_tag(P(elements[1]).children(), 'p'))

    def test_add_eventual_sibling_after_selected_sequence(self):

        selector = parse_selector('.klazz ~ p', 'selector')
        elements = create_content_from_selector(selector)

        # For the generalized sibling combinator, we want to make sure that the
        # sibling created is more than one sibling away to prove the point that this can
        # select a sibling farther away than the next one.
        self.assertEqual(P(elements[0]).attr('class'), 'klazz')
        self.assertFalse(_element_has_tag(P(elements[1]), 'p'))
        self.assertTrue(_element_has_tag(P(elements[elements.length - 1]), 'mark'))


class SelectorsGroupContentCreationTest(unittest.TestCase):

    def test_generate_content_for_multiple_selectors(self):
        selectors_group = parse_selector('.klazz, p', 'selectors_group')
        contents = create_content_from_selectors_group(selectors_group)
        self.assertEqual(
            contents['.klazz'].outer_html(),
            "<mark><div class=\"klazz\"></div></mark>"
        )
        self.assertEqual(contents['p'].outer_html(), "<mark><p></p></mark>")


class HtmlRendererTest(unittest.TestCase):

    def _render(self, contents, indent_level=1):
        return HtmlRenderer().render_html_contents(contents, indent_level=indent_level)

    def test_render_single_marked_element(self):
        html = self._render(P('<mark><p></p></mark>'))
        self.assertEqual(html, '\n'.join([
            "<span class='tutoron_selection'>",
            "&lt;p&gt;<br>",
            "&lt;/p&gt;<br>",
            "</span>",
        ]))

    def test_render_marked_element(self):
        element = P('<div><mark><p></p></mark></div>')
        html = self._render(element)
        self.assertEqual(html, '\n'.join([
            "&lt;div&gt;<br>",
            "<span class='tutoron_selection'>",
            "&nbsp;&lt;p&gt;<br>",
            "&nbsp;&lt;/p&gt;<br>",
            "</span>",
            "&lt;/div&gt;<br>",
        ]))
