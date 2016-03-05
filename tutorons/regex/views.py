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
from tutorons.common.scanner import NodeScanner
from tutorons.common.util import log_region, package_region
from tutorons.regex.extract import GrepRegexExtractor, SedRegexExtractor, JavascriptRegexExtractor,\
    ApacheConfigRegexExtractor
from tutorons.regex.explain import InvalidRegexException, visualize as regex_viz
from tutorons.regex.examples import get_examples
from tutorons.regex.render import render as regex_render
from tutorons.common.dblogger import DBLogger
from tutorons.common.extractor import Region
from tutorons.common.util import dec

logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DBLogger()


@csrf_exempt
@dec
def scan(html_doc):

    explained_regions = []
    extractors = [
        GrepRegexExtractor(),
        SedRegexExtractor(),
        JavascriptRegexExtractor(),
        ApacheConfigRegexExtractor(),
    ]
    
    rendered_regions = []
    for extractor in extractors:
        scanner = NodeScanner(extractor, ['code', 'pre'])
        regions = scanner.scan(html_doc)
        for r in regions:
            try:
                svg = regex_viz(r.pattern)
            except InvalidRegexException as e:
                logging.error("Error processing regex %s: %s", r.pattern, e)
                svg = None

            try:
                examples = get_examples(r.pattern, count=4)
            except Exception as e:
                logging.error("Error processing regex %s: %s", r.pattern, e)
                examples = None

            if examples is not None or svg is not None:
                document = regex_render(r.pattern, svg, examples)
                rendered_regions.append((r,document))
    return rendered_regions


@csrf_exempt
def explain(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    client_start_time = request.POST.get('client_start_time')
    region_logger.info("Request for text from origin: %s", origin)
    qid = db_logger.log_query(request)

    try:
        svg = regex_viz(text)
        exp = regex_render(svg)
        region = Region(HtmlDocument(text), 0, len(text) - 1, text)
        rid = db_logger.log_region(request, region)
        explained_region = package_region(region, exp, rid, qid)
        resp = json.dumps({"explained_region": explained_region,
                           "url": "http://localhost:8002/api/v1/client_query/",
                           "sq_id": qid,
                           "client_start_time": client_start_time,
                           "error": 0}, indent=2)
    except InvalidRegexException as e:
        logging.error("Error processing regular expression %s: %s", e.pattern, e.msg)
        error_template = get_template('error.html')
        error_html = error_template.render(Context({'text': text, 'type': 'regular expression'}))
        resp = json.dumps({"error": 1, "html": error_html})
    return HttpResponse(resp)
