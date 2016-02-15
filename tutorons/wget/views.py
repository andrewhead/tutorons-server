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
from tutorons.common.scanner import CommandScanner, InvalidCommandException
from tutorons.wget.explain import WgetExtractor, explain as wget_explain
from tutorons.wget.render import render as wget_render
from tutorons.common.dblogger import DBLogger
from tutorons.common.extractor import Region


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DBLogger()


@csrf_exempt
def scan(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    client_start_time = request.POST.get('client_start_time')
    region_logger.info("Request for page from origin: %s", origin)
    qid = db_logger.log_query(request)

    explained_regions = []
    document = HtmlDocument(doc_body)

    scanner = CommandScanner('wget', WgetExtractor())
    regions = scanner.scan(document)
    for r in regions:
        log_region(r, origin)
        rid = db_logger.log_region(request, r)
        try:
            exp = wget_explain(r.string)
        except InvalidCommandException as e:
            logging.error("Error processing wget command %s: %s", e.cmd, e.exception)
            continue
        document = wget_render(exp['url'], exp['opts'], exp['combo_exps'])
        explained_regions.append(package_region(r, document, rid, qid))

    return HttpResponse(json.dumps({"explained_regions": explained_regions,
                                    "url": "http://localhost:8002/api/v1/client_query/",
                                    "sq_id": qid,
                                    "client_start_time": client_start_time}, indent=2))


@csrf_exempt
def explain(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    client_start_time = request.POST.get('client_start_time')
    region_logger.info("Request for explanation for text from origin: %s", origin)
    qid = db_logger.log_query(request)

    error_template = get_template('error.html')

    try:
        exp = wget_explain(text)
        region = Region(HtmlDocument(text), 0, len(text) - 1, text)
        rid = db_logger.log_region(request, region)

    except InvalidCommandException as e:
        logging.error("Error processing wget command %s: %s", e.cmd, e.exception)
        error_html = error_template.render(Context({'text': text, 'type': 'wget command'}))
        return HttpResponse(json.dumps({"error": 1, "html": error_html}))
    else:
        exp_html = wget_render(exp['url'], exp['opts'], exp['combo_exps'])
        explained_region = package_region(region, exp_html, rid, qid)
        return HttpResponse(json.dumps({"explained_region": explained_region,
                                        "url": "http://localhost:8002/api/v1/client_query/",
                                        "sq_id": qid,
                                        "client_start_time": client_start_time,
                                        "error": 0}, indent=2))
