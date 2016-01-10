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


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')


@csrf_exempt
def scan(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    explained_regions = []
    document = HtmlDocument(doc_body)
    builtin_extractor = PythonBuiltInExtractor()

    builtin_scanner = NodeScanner(builtin_extractor, ['code', 'pre'])
    regions = builtin_scanner.scan(document)
    for r in regions:
        log_region(r, origin)
        hdr, exp, url = python_explain(r.string)
        document = python_render(r.string, hdr, exp, url)
        explained_regions.append(package_region(r, document))

    return HttpResponse(json.dumps(explained_regions, indent=2))


@csrf_exempt
def explain(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    region_logger.info("Request for text from origin: %s", origin)

    error_template = get_template('error.html')

    text = HtmlDocument(text)
    builtin_extractor = PythonBuiltInExtractor()

    builtin_scanner = NodeScanner(builtin_extractor, ['code', 'pre'])
    regions = builtin_scanner.scan(text)

    if regions[0].start_offset == 0:
        print "in explain"
        log_region(regions[0], origin)
        hdr, exp, url = python_explain(regions[0].string)
        document = python_render(regions[0].string, hdr, exp, url)
        explained_region = package_region(regions[0], document)
        return HttpResponse(json.dumps(explained_region, indent=2))
    else:
        logging.error("Error processing python built-in %s", text)
        error_html = error_template.render(Context({'text': text, 'type': 'python built-in'}))
        return HttpResponse(error_html)
