#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from tutorons.common.scanner import NodeScanner
from tutorons.css.detect import find_jquery_selector, JavascriptSelectorExtractor,\
    StylesheetSelectorExtractor, is_selector
from tutorons.css.explain import explain as css_explain
from tutorons.css.render import render as css_render
from tutorons.css.examples import generate_examples
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
        explanations = css_explain(r.string)
        examples = generate_examples(r.string)
        document = css_render(explanations, examples)
        rendered_regions.append((r, document))

    return rendered_regions


@csrf_exempt
@snippetexplain
def explain(text, edge_size):

    error_template = get_template('error.html')

    if edge_size > 0:
        text = find_jquery_selector(text, edge_size)

    if is_selector(text):
        explanations = css_explain(text)
        examples = generate_examples(text)
        explanation = css_render(explanations, examples)
    else:
        explanation = error_template.render(Context({'text': text, 'type': 'CSS selector'}))

    return explanation
