#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from py4j.java_gateway import JavaGateway
from cssselect.parser import Element, SelectorSyntaxError
import cssselect
import re

from tutorons.common.extractor import JavascriptStringExtractor
from tutorons.common.util import get_descendants
from tutorons.css.tags import HTML_TAGS
from tutorons.css.fileext import EXTENSIONS


logging.basicConfig(level=logging.INFO, format="%(message)s")

''' Our CSS explainer is implemented in Java, so we open up a gateway through Py4J for now. '''
gateway = JavaGateway()
explainer = gateway.entry_point.getExplainer()


def explain(selector):
    return explainer.explain(selector)


class CssSelectorExtractor(object):

    def __init__(self):
        self.js_string_extractor = JavascriptStringExtractor()

    def extract(self, node):
        regions = self.js_string_extractor.extract(node)
        valid_regions = [r for r in regions if is_selector(r.string)]
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
