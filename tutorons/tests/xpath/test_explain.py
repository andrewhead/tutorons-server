#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest

from tutorons.common.java.simplenlg import realiser
from tutorons.xpath.explain import explain_node_test, explain_step
from parsers.xpath.xpathLexer import xpathLexer
from parsers.xpath.xpathParser import xpathParser
from parsers.common.util import parse_plaintext


logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_xpath(xpath, rule_name):
    '''
    The selector here can be partial.  And this method returns partial
    parse results: it can be parsed as just a specific rule from the
    grammar, as specified by `rule_name`.
    '''
    return parse_plaintext(xpath, xpathLexer, xpathParser, rule_name)


class NodeTestExplanationTest(unittest.TestCase):


    def test_explain_node_type(self):
        node_type = parse_xpath('text()', 'nodeTest')
        clause = explain_node_test(node_type)
        self.assertEqual(
            str(realiser.realise(clause)),
            "text nodes"
        )

        node_type = parse_xpath('comment()', 'nodeTest')
        clause = explain_node_test(node_type)
        self.assertEqual(
            str(realiser.realise(clause)),
            "comment nodes"
        )

        node_type = parse_xpath('processing-instruction()', 'nodeTest')
        clause = explain_node_test(node_type)
        self.assertEqual(
            str(realiser.realise(clause)),
            "processing-instruction nodes"
        )

        node_type = parse_xpath('node()', 'nodeTest')
        clause = explain_node_test(node_type)
        self.assertEqual(
            str(realiser.realise(clause)),
            "all nodes"
        )

    def test_explain_html_name_test(self):
        html_name_test = parse_xpath('p', 'nodeTest')
        clause = explain_node_test(html_name_test)
        self.assertEqual(
            str(realiser.realise(clause)),
            "paragraphs"
        )

    def test_explain_name_test(self):
        name_test = parse_xpath('lang', 'nodeTest')
        clause = explain_node_test(name_test)
        self.assertEqual(
            str(realiser.realise(clause)),
            "'lang' nodes"
        )


class AxisSepcifierExplanationTest(unittest.TestCase):

    def test_explain_child(self):
            axis_spec = parse_xpath('child::text()', 'step')
            clause = explain_step(axis_spec)
            self.assertEqual(
                str(realiser.realise(clause)),
                "children of text nodes"
            )

    def test_explain_self(self):
            axis_spec = parse_xpath('self::text()', 'step')
            clause = explain_step(axis_spec)
            self.assertEqual(
                str(realiser.realise(clause)),
                "halp?"
            )

    def test_explain_ancestors_or_self(self):
            axis_spec = parse_xpath('ancestor-or-self::text()', 'step')
            clause = explain_step(axis_spec)
            self.assertEqual(
                str(realiser.realise(clause)),
                "curr node and ancestors of text nodes"
            )

    def test_explain_descendants_or_self(self):
            axis_spec = parse_xpath('descendant-or-self::text()', 'step')
            clause = explain_step(axis_spec)
            self.assertEqual(
                str(realiser.realise(clause)),
                "curr node and descendants of text nodes"
            )

    def test_explain_attribute(self):
            axis_spec = parse_xpath('@text', 'step')
            clause = explain_step(axis_spec)
            self.assertEqual(
                str(realiser.realise(clause)),
                "nodes with a text attribute"
            )


# class ClassExplanationTest(unittest.TestCase):

#     def test_explain_class(self):
#         class_ = parse_selector('.klazz', 'class_')
#         clause = explain_class(class_)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "belongs to class 'klazz'"
#         )


# class HashExplanationTest(unittest.TestCase):

#     def test_explain_hash(self):
#         hash_ = parse_selector('#my-id', 'hash_')
#         clause = explain_hash(hash_)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "has ID 'my-id'"
#         )


# class UniversalSelectorExplanationTest(unittest.TestCase):

#     def test_explain_universal_selector(self):
#         universal = parse_selector('*', 'universal')
#         noun = explain_universal(universal)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             'elements'
#         )

#     def test_ignore_namespace(self):
#         universal = parse_selector('namespace|*', 'universal')
#         noun = explain_universal(universal)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             'elements'
#         )


# class TypeSelectorExplanationTest(unittest.TestCase):

#     def test_explain_element_with_verbatim_name(self):
#         type_selector = parse_selector('html', 'type_selector')
#         noun = explain_type_selector(type_selector)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             '\'html\' elements'
#         )

#     def test_explain_element_with_lookup_name(self):
#         type_selector = parse_selector('p', 'type_selector')
#         noun = explain_type_selector(type_selector)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             'paragraphs'
#         )

#     def test_ignore_namespace(self):
#         type_selector = parse_selector('namespace|p', 'type_selector')
#         noun = explain_type_selector(type_selector)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             'paragraphs'
#         )


# class PseudoclassExplanationTest(unittest.TestCase):

#     def test_explain_property_pseudoclass(self):
#         pseudo = parse_selector(':checked', 'pseudo')
#         clause = explain_pseudo(pseudo)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             'is checked'
#         )

#     def test_explain_unknown_functional_pseudoclass_with_simple_default(self):
#         pseudo = parse_selector(':ath-child(4n)', 'pseudo')
#         clause = explain_pseudo(pseudo)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             'satisfies the function \'ath-child(4n)\''
#         )

#     def test_explain_pseudoelement(self):
#         pseudo = parse_selector('::before', 'pseudo')
#         noun = explain_pseudo(pseudo)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             'generated content before the element\'s content'
#         )

#     def test_explain_unknown_pseudoelement_with_simple_default(self):
#         pseudo = parse_selector('::cheese', 'pseudo')
#         noun = explain_pseudo(pseudo)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             'content that matches the pseudo-element \'::cheese\''
#         )

#     # While the above tests are more for testing generic functionality, the test
#     # cases below are for checking that special pseudo selectors are described correctly.

#     def test_explain_attr_functional_pseudoelement(self):
#         pseudo = parse_selector('::attr(href)', 'pseudo')
#         noun = explain_pseudo(pseudo)
#         self.assertEqual(
#             str(realiser.realise(noun)),
#             'the value of the \'href\' attribute'
#         )

#     def test_explain_text_pseudoelement(self):
#         pseudo = parse_selector('::text', 'pseudo')
#         noun = explain_pseudo(pseudo)
#         self.assertEqual(str(realiser.realise(noun)), 'text content')


# class SimpleSelectorSequenceExplanationTest(unittest.TestCase):

#     def test_explain_multiple_selectors_with_conjunction(self):
#         sequence = parse_selector('p.klazz[href^=\'http://\']', 'simple_selector_sequence')
#         clause = explain_simple_selector_sequence(sequence)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "all paragraphs that belong to class 'klazz' and that " +
#             "have a link that starts with 'http://'"
#         )

#     def test_shift_subject_with_pseudoelement_and_class(self):
#         sequence = parse_selector('.klazz::before', 'simple_selector_sequence')
#         clause = explain_simple_selector_sequence(sequence)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "generated content before the element's content for " +
#             "all elements that belong to class 'klazz'"
#         )

#     def test_all_adjective_goes_before_type_adjective(self):
#         sequence = parse_selector('unknown_element', 'simple_selector_sequence')
#         clause = explain_simple_selector_sequence(sequence)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "all 'unknown_element' elements"
#         )


# class SelectorExplanationTest(unittest.TestCase):
#     '''
#     Note that once we describe multiple selectors, we now only describe 'all'
#     elements for the final selection, and lose the 'all' qualifier for every
#     selector sequence that a later selector sequence is chosen 'from'.
#     '''
#     def test_explain_descendant_selection(self):
#         selector = parse_selector('.klazz p', 'selector')
#         clause = explain_selector(selector)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "all paragraphs from elements that belong to class 'klazz'"
#         )

#     def test_explain_child_selection(self):
#         selector = parse_selector('.klazz > p', 'selector')
#         clause = explain_selector(selector)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "all paragraphs that are children of elements that belong to class 'klazz'"
#         )

#     def test_explain_sibling_selection(self):
#         selector = parse_selector('.klazz + p', 'selector')
#         clause = explain_selector(selector)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "all paragraphs that are siblings of and that appear right after " +
#             "elements that belong to class 'klazz'"
#         )

#     def test_explain_generalized_sibling_selection(self):
#         selector = parse_selector('.klazz ~ p', 'selector')
#         clause = explain_selector(selector)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "all paragraphs that are siblings of and that eventually appear " +
#             "after elements that belong to class 'klazz'"
#         )


# class SelectorsGroupExplanationTest(unittest.TestCase):

#     def test_explain_selectors_group_with_list_of_explanations(self):
#         selectors_group = parse_selector('p, p > .klazz', 'selectors_group')
#         clauses = explain_selectors_group(selectors_group)
#         self.assertEqual(len(clauses), 2)
#         self.assertEqual(
#             str(realiser.realise(clauses['p'])),
#             "all paragraphs"
#         )
#         self.assertEqual(
#             str(realiser.realise(clauses['p > .klazz'])),
#             "all elements that belong to class 'klazz' that are children of paragraphs"
#         )