#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from tutorons.common.scanner import NodeScanner
from tutorons.css.detect import find_jquery_selector
from tutorons.css.explain import JavascriptSelectorExtractor, StylesheetSelectorExtractor
from tutorons.css.explain import explain as css_explain, is_selector
from tutorons.css.render import render as css_render
from parsers.css.examples.examplegen import get_example as css_example
from tutorons.common.dblogger import DbLogger
from tutorons.common.views import pagescan, snippetexplain


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DbLogger()


@csrf_exempt
@pagescan
def scan(html_doc):

    js_extractor = JavascriptSelectorExtractor()
    stylesheet_extractor = StylesheetSelectorExtractor()

    js_scanner = NodeScanner(js_extractor, ['code', 'pre'])
    stylesheet_scanner = NodeScanner(stylesheet_extractor, ['code', 'pre', 'div'])
    regions = js_scanner.scan(html_doc) + stylesheet_scanner.scan(html_doc)
    rendered_regions = []
    for r in regions:
        exp = css_explain(r.string)
        example = css_example(r.string)
        document = css_render(exp, example)
        rendered_regions.append((r, document))

    return rendered_regions


@csrf_exempt
@snippetexplain
def explain(text, edge_size):

    error_template = get_template('error.html')

    if edge_size > 0:
        text = find_jquery_selector(text, edge_size)

    if is_selector(text):
        exp = css_explain(text)
        example = css_example(text)
        explanation = css_render(exp, example)
    else:
        explanation = error_template.render(Context({'text': text, 'type': 'CSS selector'}))

    return explanation
