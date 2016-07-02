#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from cssselect.parser import Element, SelectorSyntaxError
import cssselect
import re
from bs4 import BeautifulSoup
import tinycss

from tutorons.common.extractor import JavascriptStringExtractor
from tutorons.common.extractor import Region

from tutorons.common.util import get_descendants
from tutorons.css.tags import HTML_TAGS
from tutorons.css.fileext import EXTENSIONS


logging.basicConfig(level=logging.INFO, format="%(message)s")


def filter_non_ascii(c):
    if ord(c) > 127:
        return ' '
    return c


class JavascriptSelectorExtractor(object):

    def __init__(self):
        self.js_string_extractor = JavascriptStringExtractor()

    def extract(self, node):
        regions = self.js_string_extractor.extract(node)
        valid_regions = [r for r in regions if is_selector(r.string)]
        return valid_regions


class StylesheetSelectorExtractor(object):

    def extract(self, node):
        textfield = ''.join(map(filter_non_ascii, node.text))
        textfield_as_list = textfield.split('\n')
        ss_offset = 0

        # sets textfield to the text in the style tag, if exists and adjusts the offset
        if BeautifulSoup(textfield).style:
            ss_offset = textfield.find("<style>") + len("<style>")
            textfield = ''.join(map(filter_non_ascii, BeautifulSoup(textfield).style.text))
            textfield_as_list = textfield.split('\n')

        # parses textfield as a stylesheet
        parser = tinycss.make_parser()
        stylesheet = parser.parse_stylesheet(textfield)
        valid_regions = []

        # calculate the start index of the selector
        for rule in stylesheet.rules:
            sel = rule.selector
            ss_start = ss_offset
            if sel.line > 1:
                for l in xrange(sel.line - 1):
                    # add 1 to account for newline characters
                    ss_start += len(textfield_as_list[l]) + 1
            ss_start += sel.column - 1
            sel = rule.selector.as_css()
            if rule.declarations:
                valid_regions.append(Region(node, ss_start, ss_start + len(sel) - 1, sel))

        # check if the regions found contain valid selectors
        for region in valid_regions:
            if not is_selector(region.string):
                valid_regions.remove(region)
        return valid_regions


def is_selector(string):
    ''' Check to see if string represents valid HTML selector. '''
    try:
        # cssselect doesn't like links, so we replace them.
        string = re.sub(r"(href.=)([^\]]*)\]", r"\1fakelink]", string)
        tree = cssselect.parse(string)
    except SelectorSyntaxError:
        return False
    return _do_elements_have_standard_tags(tree) and not _is_file_extension(tree)


def _is_file_extension(selector_tree):
    '''
    Check to see if string is a file extension.
    We do this by seeing if the tree consists of a single class with the name
    of a file extension without a named element.
    '''
    if len(selector_tree) > 0 and hasattr(selector_tree[0], 'parsed_tree'):
        pt = selector_tree[0].parsed_tree
        if hasattr(pt, 'class_name'):
            cn = pt.class_name
            if ((cn.upper() in EXTENSIONS or cn.lower() in EXTENSIONS) and
                    pt.selector.element is None):
                return True
    return False


def _do_elements_have_standard_tags(selector_tree):
    selector_parts = get_descendants(selector_tree)
    for part in selector_parts:
        if isinstance(part, Element):
            if part.element not in HTML_TAGS:
                return False
    return True


def find_jquery_selector(string, edge_size):
    '''
    This routine attempts to find a Javascript string that is the closest to a user's original
    selection, where the original selection is contained within the string, but with additional
    context on each side 'edge_size' big.
    edge_size must be > 1 for this method to work properly.
    Returns the original selection (without context) if no Javascript string was found

    To find the string closest to the user's selection, it does the following:
    1. Finds all pairs of quotation marks (single or double quotes)
    2. Picks the pair of quotation marks closest to the user's original selection
    3. Returns the string encapsulated within those quotation marks
    '''
    # The ideal quotation position would be directly outside the user's original selection
    # (i.e., the first character of the edge right outside the original string)
    target = [edge_size - 1, len(string) - edge_size]
    quote_pairs = []
    double_quote = None
    single_quote = None

    # Discover all pairs of quotation marks
    for i, c in enumerate(string):
        if c == "'":
            if single_quote is not None:
                quote_pairs.append((single_quote, i))
            single_quote = i
        elif c == '"':
            if double_quote is not None:
                quote_pairs.append((double_quote, i))
            double_quote = i

    # If there are no quotation pairs, then return the original string
    if len(quote_pairs) == 0:
        return string[edge_size:len(string) - edge_size]

    # Detect the pair of quotes closest to the original region
    dist = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
    distances = {qp: dist(qp, target) for qp in quote_pairs}
    best = min(distances.items(), key=lambda item: item[1])
    best_qp = best[0]
    return string[best_qp[0] + 1:best_qp[1]]
