#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest

from tutorons.common.java.simplenlg import factory as nlg_factory, realiser
from tutorons.xpath.explain import explain_node_test, explain_step, explain_absolute_location_path, \
    explain_relative_location_path
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

        # processing-instruction takes in an argument
        # node_type = parse_xpath('processing-instruction()', 'nodeTest')
        # clause = explain_node_test(node_type)
        # self.assertEqual(
        #     str(realiser.realise(clause)),
        #     "processing-instruction nodes"
        # )


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
        clause = nlg_factory.createNounPhrase()
        explain_step(axis_spec, clause)
        self.assertEqual(
            str(realiser.realise(clause)),
            "text nodes"
        )

    def test_explain_ancestor(self):
        axis_spec = parse_xpath('ancestor::text()', 'step')
        clause = nlg_factory.createNounPhrase()
        explain_step(axis_spec, clause)
        self.assertEqual(
            str(realiser.realise(clause)),
            "ancestors of text nodes"
        )

# ## umm weird objct return stuff help
#     def test_explain_self(self):
#         axis_spec = parse_xpath('self::text()', 'step')
#         clause = nlg_factory.createNounPhrase()
#         clause = explain_step(axis_spec, clause)
#         self.assertEqual(
#             str(realiser.realise(clause)),
#             "if they are text nodes"
#         )

    def test_explain_ancestors_or_self(self):
        axis_spec = parse_xpath('ancestor-or-self::text()', 'step')
        clause = nlg_factory.createNounPhrase()
        explain_step(axis_spec, clause)
        self.assertEqual(
            str(realiser.realise(clause)),
            "text nodes and ancestors of such nodes"
        )

    def test_explain_descendants_or_self(self):
        axis_spec = parse_xpath('descendant-or-self::text()', 'step')
        clause = nlg_factory.createNounPhrase()
        explain_step(axis_spec, clause)
        self.assertEqual(
            str(realiser.realise(clause)),
            "text nodes and descendants of such nodes"
        )

    def test_explain_attribute(self):
        axis_spec = parse_xpath('@name', 'step')
        clause = nlg_factory.createNounPhrase()
        explain_step(axis_spec, clause)
        self.assertEqual(
            str(realiser.realise(clause)),
            "'name' attributes"
        )

    def test_simple_multiple_steps(self):
        multiple_steps = parse_xpath('/child::text()/descendant::comment()', 'absoluteLocationPathNoroot')
        clause = explain_absolute_location_path(multiple_steps)
        self.assertEqual(
            str(realiser.realise(clause)),
            "descendants of comment nodes from text nodes from the root node"
        )
    
    def test_complex_multiple_steps(self):
            multiple_steps = parse_xpath('//ancestor-or-self::text()/self::comment()', 'absoluteLocationPathNoroot')
            clause = explain_absolute_location_path(multiple_steps)
            self.assertEqual(
                str(realiser.realise(clause)),
                "text nodes and ancestors of such nodes from anywhere in the tree if they are comment nodes"
            )
              # from text nodes and ancestors of such nodes from anywhere in the tree
#             # 'if such nodes are comment nodes from text nodes and ancestors of such nodes from anywhere in the tree' 
#             # != 'text nodes and ancestors of such nodes from anywhere in the tree if such nodes are comment nodes'

#             # need to append returned clause to previous explained clause and remove the 'from' that joins the 2 would be clauses
class LocationPathExplanationTest(unittest.TestCase):

    def test_explain_root(self):
        abs_path = parse_xpath('/text()', 'absoluteLocationPathNoroot')
        clause = explain_absolute_location_path(abs_path)
        self.assertEqual(
            str(realiser.realise(clause)),
            "text nodes from the root node"
        )

    def test_explain_descendant(self):
        abs_path = parse_xpath('//text()', 'absoluteLocationPathNoroot')
        clause = explain_absolute_location_path(abs_path)
        self.assertEqual(
            str(realiser.realise(clause)),
            "text nodes from anywhere in the tree"
        )  

    def test_multiple_steps(self):
        multiple_steps = parse_xpath('/text()/comment()', 'absoluteLocationPathNoroot')
        clause = explain_absolute_location_path(multiple_steps)
        self.assertEqual(
            str(realiser.realise(clause)),
            "comment nodes from text nodes from the root node"
        )


class RelativeLocationPathExplanationTest(unittest.TestCase):

    def test_abbreviated_step(self):
        abbreviated_step = parse_xpath('text()/./@lang', 'relativeLocationPath')
        clause = explain_relative_location_path(abbreviated_step)
        self.assertEqual(
            str(realiser.realise(clause)),
            "'lang' attributes from text nodes"
        )

    def test_parent_abbreviated_step(self):
        abbreviated_step = parse_xpath('text()/../@lang', 'relativeLocationPath')
        clause = explain_relative_location_path(abbreviated_step)
        self.assertEqual(
            str(realiser.realise(clause)),
            "'lang' attributes from parents of text nodes"
        )

    def test_relative_step(self):
        abbreviated_step = parse_xpath('comment()//@lang', 'relativeLocationPath')
        clause = explain_relative_location_path(abbreviated_step)
        self.assertEqual(
            str(realiser.realise(clause)),
            "'lang' attributes from descendants of comment nodes"
        )