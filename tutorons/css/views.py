#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from tutorons.common.htmltools import HtmlDocument
from tutorons.common.util import log_region, package_region
from tutorons.common.scanner import NodeScanner
from tutorons.css.detect import find_jquery_selector
from tutorons.css.explain import JavascriptSelectorExtractor, StylesheetSelectorExtractor
from tutorons.css.explain import explain as css_explain, is_selector
from tutorons.css.render import render as css_render
from parsers.css.examples.examplegen import get_example as css_example
from tutorons.common.dblogger import DBLogger
from tutorons.common.extractor import Region
from tutorons.common.util import dec

logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DBLogger()


@csrf_exempt
@dec
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
def explain(request):

    text = request.POST.get('text')
    edge_size = int(request.POST.get('edge_size', 0))
    origin = request.POST.get('origin')
    client_start_time = request.POST.get('client_start_time')
    region_logger.info("Request for text from origin: %s", origin)
    qid = db_logger.log_query(request)

    error_template = get_template('error.html')

    if edge_size > 0:
        text = find_jquery_selector(text, edge_size)

    if is_selector(text):
        region = Region(HtmlDocument(text), 0, len(text) - 1, text)
        rid = db_logger.log_region(request, region)
        exp = css_explain(text)
        example = css_example(text)
        exp_html = css_render(exp, example)
        explained_region = package_region(region, exp_html, rid, qid)

        return HttpResponse(json.dumps({"explained_region": explained_region,
                                        "url": "http://localhost:8002/api/v1/client_query/",
                                        "sq_id": qid,
                                        "client_start_time": client_start_time,
                                        "error": 0}, indent=2))

    else:
        logging.error("Error processing CSS selector %s", text)
        error_html = error_template.render(Context({'text': text, 'type': 'CSS selector'}))
        return HttpResponse(json.dumps({"error": 1, "html": error_html}))
