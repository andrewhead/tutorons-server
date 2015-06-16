#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from py4j.java_gateway import JavaGateway
from cssselect.parser import Element, SelectorSyntaxError
import cssselect
import re

from tutorons.common.extractor import JavascriptStringExtractor
from tutorons.common.util import get_descendants, log_region
from tutorons.css.tags import HTML_TAGS


logging.basicConfig(level=logging.INFO, format="%(message)s")

''' Our CSS explainer is implemented in Java, so we open up a gateway through Py4J for now. '''
gateway = JavaGateway()
explainer = gateway.entry_point.getExplainer()


class CssSelectorExtractor(object):

    def __init__(self):
        self.js_string_extractor = JavascriptStringExtractor()

    def extract(self, node):
        regions = self.js_string_extractor.extract(node)
        valid_regions = [r for r in regions if self._is_selector(r.string)]
        [log_region(r) for r in valid_regions]
        return valid_regions

    def _is_selector(self, string):
        ''' Check to see if string represents valid HTML selector. '''
        try:
            # cssselect doesn't like links, so we replace them.
            string = re.sub(r"(href.=)([^\]]*)\]", r"\1fakelink]", string)
            tree = cssselect.parse(string)
            selector_parts = get_descendants(tree)
            for part in selector_parts:
                if isinstance(part, Element):
                    if part.element not in HTML_TAGS:
                        return False
            return True
        except SelectorSyntaxError:
            return False


def explain(selector):
    return explainer.explain(selector)
