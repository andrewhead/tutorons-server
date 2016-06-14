#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest

from tutorons.common.java.simplenlg import realiser
from tutorons.css.explain import explain_attribute, explain_class, explain_hash,\
    explain_type_selector, explain_universal, explain_pseudo, explain_simple_selector_sequence,\
    explain_selector, explain_selectors_group
from parsers.css.CssLexer import CssLexer
from parsers.css.CssParser import CssParser
from parsers.common.util import parse_plaintext


logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_selector(selector, rule_name):
    '''
    The selector here can be partial.  And this method returns partial
    parse results: it can be parsed as just a specific rule from the
    grammar, as specified by `rule_name`.
    '''
    return parse_plaintext(selector, CssLexer, CssParser, rule_name)


class AttributeExplanationTest(unittest.TestCase):

    def test_explain_name_attribute_by_default(self):
        attribute = parse_selector('[myattr=foo]', 'attribute')
        clause = explain_attribute(attribute)
        self.assertEqual(
            str(realiser.realise(clause)),
            "has a 'myattr' attribute that equals 'foo'"
        )

    def test_attribute_special_names(self):
        attribute = parse_selector('[href^=\'http://\']', 'attribute')
        clause = explain_attribute(attribute)
        self.assertEqual(
            str(realiser.realise(clause)),
            "has a link that starts with 'http://'"
        )


class ClassExplanationTest(unittest.TestCase):

    def test_explain_class(self):
        class_ = parse_selector('.klazz', 'class_')
        clause = explain_class(class_)
        self.assertEqual(
            str(realiser.realise(clause)),
            "belongs to class 'klazz'"
        )


class HashExplanationTest(unittest.TestCase):

    def test_explain_hash(self):
        hash_ = parse_selector('#my-id', 'hash_')
        clause = explain_hash(hash_)
        self.assertEqual(
            str(realiser.realise(clause)),
            "has ID 'my-id'"
        )


class UniversalSelectorExplanationTest(unittest.TestCase):

    def test_explain_universal_selector(self):
        universal = parse_selector('*', 'universal')
        noun = explain_universal(universal)
        self.assertEqual(
            str(realiser.realise(noun)),
            'elements'
        )

    def test_ignore_namespace(self):
        universal = parse_selector('namespace|*', 'universal')
        noun = explain_universal(universal)
        self.assertEqual(
            str(realiser.realise(noun)),
            'elements'
        )


class TypeSelectorExplanationTest(unittest.TestCase):

    def test_explain_element_with_verbatim_name(self):
        type_selector = parse_selector('html', 'type_selector')
        noun = explain_type_selector(type_selector)
        self.assertEqual(
            str(realiser.realise(noun)),
            '\'html\' elements'
        )

    def test_explain_element_with_lookup_name(self):
        type_selector = parse_selector('p', 'type_selector')
        noun = explain_type_selector(type_selector)
        self.assertEqual(
            str(realiser.realise(noun)),
            'paragraphs'
        )

    def test_ignore_namespace(self):
        type_selector = parse_selector('namespace|p', 'type_selector')
        noun = explain_type_selector(type_selector)
        self.assertEqual(
            str(realiser.realise(noun)),
            'paragraphs'
        )


class PseudoclassExplanationTest(unittest.TestCase):

    def test_explain_property_pseudoclass(self):
        pseudo = parse_selector(':checked', 'pseudo')
        clause = explain_pseudo(pseudo)
        self.assertEqual(
            str(realiser.realise(clause)),
            'is checked'
        )

    def test_explain_unknown_functional_pseudoclass_with_simple_default(self):
        pseudo = parse_selector(':ath-child(4n)', 'pseudo')
        clause = explain_pseudo(pseudo)
        self.assertEqual(
            str(realiser.realise(clause)),
            'satisfies the function \'ath-child(4n)\''
        )

    def test_explain_pseudoelement(self):
        pseudo = parse_selector('::before', 'pseudo')
        noun = explain_pseudo(pseudo)
        self.assertEqual(
            str(realiser.realise(noun)),
            'generated content before the element\'s content'
        )

    def test_explain_unknown_pseudoelement_with_simple_default(self):
        pseudo = parse_selector('::cheese', 'pseudo')
        noun = explain_pseudo(pseudo)
        self.assertEqual(
            str(realiser.realise(noun)),
            'content matching the pseudo-element \'::cheese\''
        )


class SimpleSelectorSequenceExplanationTest(unittest.TestCase):

    def test_explain_multiple_selectors_with_conjunction(self):
        sequence = parse_selector('p.klazz[href^=\'http://\']', 'simple_selector_sequence')
        clause = explain_simple_selector_sequence(sequence)
        self.assertEqual(
            str(realiser.realise(clause)),
            "all paragraphs that belong to class 'klazz' and that " +
            "have a link that starts with 'http://'"
        )

    def test_shift_subject_with_pseudoelement(self):
        sequence = parse_selector('.klazz::before', 'simple_selector_sequence')
        clause = explain_simple_selector_sequence(sequence)
        self.assertEqual(
            str(realiser.realise(clause)),
            "generated content before the element's content for " +
            "all elements that belong to class 'klazz'"
        )


class SelectorExplanationTest(unittest.TestCase):
    '''
    Note that once we describe multiple selectors, we now only describe 'all'
    elements for the final selection, and lose the 'all' qualifier for every
    selector sequence that a later selector sequence is chosen 'from'.
    '''
    def test_explain_descendant_selection(self):
        selector = parse_selector('.klazz p', 'selector')
        clause = explain_selector(selector)
        self.assertEqual(
            str(realiser.realise(clause)),
            "all paragraphs from elements that belong to class 'klazz'"
        )

    def test_explain_child_selection(self):
        selector = parse_selector('.klazz > p', 'selector')
        clause = explain_selector(selector)
        self.assertEqual(
            str(realiser.realise(clause)),
            "all paragraphs that are children of elements that belong to class 'klazz'"
        )

    def test_explain_sibling_selection(self):
        selector = parse_selector('.klazz + p', 'selector')
        clause = explain_selector(selector)
        self.assertEqual(
            str(realiser.realise(clause)),
            "all paragraphs that are siblings of and that appear right after " +
            "elements that belong to class 'klazz'"
        )

    def test_explain_generalized_sibling_selection(self):
        selector = parse_selector('.klazz ~ p', 'selector')
        clause = explain_selector(selector)
        self.assertEqual(
            str(realiser.realise(clause)),
            "all paragraphs that are siblings of and that eventually appear " +
            "after elements that belong to class 'klazz'"
        )


class SelectorsGroupExplanationTest(unittest.TestCase):

    def test_explain_selectors_group_with_list_of_explanations(self):
        selectors_group = parse_selector('p, p > .klazz', 'selectors_group')
        clauses = explain_selectors_group(selectors_group)
        self.assertEqual(len(clauses), 2)
        self.assertEqual(
            str(realiser.realise(clauses['p'])),
            "all paragraphs"
        )
        self.assertEqual(
            str(realiser.realise(clauses['p > .klazz'])),
            "all elements that belong to class 'klazz' that are children of paragraphs"
        )

"""
class SelectorExplanationTest(unittest.TestCase):

    def test_explain_nested_elements(self):
        exp = explain('div a')
        self.assertIn("chooses links from containers", exp)

    def test_explain_classes(self):
        exp = explain('div.klazz')
        self.assertIn("chooses containers of class 'klazz'", exp)

    def test_explain_ids(self):
        exp = explain('div#ident')
        self.assertIn("chooses a container with the ID 'ident'", exp)

    def test_explain_pseudoclass_as_state(self):
        exp = explain('input:checked')
        self.assertIn("chooses checked inputs", exp)
        exp = explain('input:hidden')
        self.assertIn("chooses hidden inputs", exp)
        exp = explain('input:visible')
        self.assertIn("chooses visible inputs", exp)
        exp = explain('input:enabled')
        self.assertIn("chooses enabled inputs", exp)
        exp = explain('a:active')
        self.assertIn("chooses active links", exp)
        exp = explain('a:visited')
        self.assertIn("chooses visited links", exp)
        exp = explain('div:empty')
        self.assertIn("chooses empty containers", exp)
        # Tricky ones requiring manual manipulation
        exp = explain('a:focus')
        self.assertIn("chooses in-focus links", exp)
        exp = explain('a:hover')
        self.assertIn("chooses hovered-over links", exp)

    def test_explain_pseudoclass_as_pseudoclass(self):
        exp = explain('input:checked')
        self.assertIn("chooses checked inputs", exp)

    def test_explain_class(self):
        exp = explain('.watch-view-count')
        self.assertEqual(
            exp, "The selector '.watch-view-count' chooses elements of class " +
            "'watch-view-count'.")

    def test_explain_pre(self):
        exp = explain('pre')
        self.assertIn("preformatted text", exp)

    def test_explain_img(self):
        exp = explain('img')
        self.assertIn("images", exp)

    def test_explain_camelcase(self):
        exp = explain('.watchView')
        self.assertIn('.watchView', exp)

    def test_explanations_regression_set(self):

        # Regression tests of the original strings that we set out to test.
        # At some point these should be refactored into tests that test for
        # specific features (e.g., coverage of element types and tree structures).
        self.assertEqual(
            explain("div.featured a"),
            "The selector 'div.featured a' chooses links from containers of class 'featured'."
        )
        self.assertEqual(
            explain("div.video-summary-data a[href^=/video]"),
            "The selector 'div.video-summary-data a[href^=/video]' chooses links with URLs " +
            "starting with '/video' from containers of class 'video-summary-data'."
        )
        self.assertEqual(
            explain("p.introduction::text"),
            "The selector 'p.introduction::text' chooses text from paragraphs " +
            "of class 'introduction'."
        )
        self.assertEqual(
            explain("div#videobox h3"),
            "The selector 'div#videobox h3' chooses headers (of level 3) " +
            "from a container with the ID 'videobox'."
        )
        self.assertEqual(
            explain(".watch-view-count"),
            "The selector '.watch-view-count' chooses elements of class 'watch-view-count'."
        )
        self.assertEqual(
            explain(".form_box input:checked"),
            "The selector '.form_box input:checked' chooses checked inputs from " +
            "elements of class 'form_box'."
        )
        self.assertEqual(
            explain("input:focus"),
            "The selector 'input:focus' chooses in-focus inputs."
        )
"""
