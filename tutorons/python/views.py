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
from tutorons.python.detect import PythonBuiltInExtractor
from tutorons.python.explain import explain as python_explain
from tutorons.python.render import render as python_render
from tutorons.python.builtins import explanations
from tutorons.common.extractor import Region
from tutorons.common.dblogger import DBLogger
from tutorons.common.util import dec

logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DBLogger()


@csrf_exempt
@dec
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
def explain(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    client_start_time = request.POST.get('client_start_time')
    region_logger.info("Request for text from origin: %s", origin)
    qid = db_logger.log_query(request)

    error_template = get_template('error.html')

    if text in explanations:
        region = Region(HtmlDocument(text), 0, len(text) - 1, text)
        log_region(region, origin)
        rid = db_logger.log_region(request, region)
        hdr, exp, url = python_explain(text)
        exp_html = python_render(text, hdr, exp, url)
        db_logger.update_server_end_time(qid)
        explained_region = package_region(region, exp_html, rid, qid)

        return HttpResponse(json.dumps({"explained_region": explained_region,
                                        "url": "http://localhost:8002/api/v1/client_query/",
                                        "sq_id": qid,
                                        "client_start_time": client_start_time,
                                        "error": 0}, indent=2))
    else:
        logging.error("Error processing python built-in %s", text)
        error_html = error_template.render(Context({'text': text, 'type': 'python built-in'}))
        return HttpResponse(json.dumps({"error": 1, "html": error_html}))
