#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from tutorons.common.scanner import NodeScanner
from tutorons.python.detect import PythonBuiltInExtractor
from tutorons.python.explain import explain as python_explain
from tutorons.python.render import render as python_render
from tutorons.python.builtins import explanations
from tutorons.common.dblogger import DbLogger
from tutorons.common.views import pagescan, snippetexplain


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DbLogger()


@csrf_exempt
@pagescan
def scan(html_doc):
    builtin_extractor = PythonBuiltInExtractor()
    builtin_scanner = NodeScanner(builtin_extractor, ['code', 'pre'])
    regions = builtin_scanner.scan(html_doc)
    rendered_regions = []
    for r in regions:
        # log_region(r, origin)
        hdr, exp, url = python_explain(r.string)
        document = python_render(r.string, hdr, exp, url)
        rendered_regions.append((r, document))
    # db_logger.update_server_end_time(qid)
    return rendered_regions


@csrf_exempt
@snippetexplain
def explain(text, edge_size):

    error_template = get_template('error.html')

    if text in explanations:
        hdr, exp, url = python_explain(text)
        explanation = python_render(text, hdr, exp, url)
    else:
        logging.error("Error processing python built-in %s", text)
        explanation = error_template.render(Context({'text': text, 'type': 'python built-in'}))

    return explanation
