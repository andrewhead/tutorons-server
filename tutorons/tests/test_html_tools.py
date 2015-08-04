#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
from tutorons.common.htmltools import HtmlDocument
from tutorons.common.htmltools import fill_empty_lines, get_css_selector


logging.basicConfig(level=logging.INFO, format="%(message)s")


class FillEmptyHtmlTest(unittest.TestCase):

    def test_fill_empty_lines(self):
        text = '\n'.join([
            '<html>',
            '  <body>',
            '    <span>text</span>',
            '',
            '  </body>',
            '</html>',
        ])
        filled = fill_empty_lines(text, 'p')
        self.assertEqual(filled, '\n'.join([
            '<html>',
            '  <body>',
            '    <span>text</span>',
            '<p></p>',
            '  </body>',
            '</html>',
        ]))


class GetPathTest(unittest.TestCase):

    def test_get_path_single_ancestry(self):
        doc = '\n'.join([
            '<html>',
            '   <body>',
            '       <p></p>',
            '   </body>',
            '</html>',
        ])
        soup = HtmlDocument(doc)
        p = soup.p
        selector = get_css_selector(p)
        self.assertEqual(selector, 'HTML > BODY:nth-of-type(1) > P:nth-of-type(1)')

    def test_get_path_2nd_child(self):
        doc = '\n'.join([
            '<html>',
            '   <body>',
            '       <p></p>',
            '       <p></p>',
            '   </body>',
            '</html>',
        ])
        soup = HtmlDocument(doc)
        p = soup.find_all('p')[1]
        selector = get_css_selector(p)
        self.assertEqual(selector, 'HTML > BODY:nth-of-type(1) > P:nth-of-type(2)')

    def test_do_not_count_children_of_different_type(self):
        doc = '\n'.join([
            '<html>',
            '   <body>',
            '       <p></p>',
            '       <ul></ul>',  # this is not a <p> element
            '       <p></p>',
            '   </body>',
            '</html>',
        ])
        soup = HtmlDocument(doc)
        p = soup.find_all('p')[1]
        selector = get_css_selector(p)
        self.assertEqual(selector, 'HTML > BODY:nth-of-type(1) > P:nth-of-type(2)')

    def test_get_path_multiple_levels_nth_child(self):
        doc = '\n'.join([
            '<html>',
            '   <body>',
            '       <div>',
            '           <p></p>',
            '       </div>',
            '       <div>'
            '           <p></p>',
            '           <p></p>',
            '           <p></p>',
            '       </div>',
            '       <div></div>',
            '   </body>',
            '</html>',
        ])
        soup = HtmlDocument(doc)
        p = soup.find_all('div')[1].find_all('p')[2]
        selector = get_css_selector(p)
        self.assertEqual(
            selector,
            'HTML > BODY:nth-of-type(1) > ' +
            'DIV:nth-of-type(2) > P:nth-of-type(3)')


if __name__ == '__main__':
    unittest.main()
