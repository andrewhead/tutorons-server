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


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')


@csrf_exempt
def scan(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    explained_regions = []
    document = HtmlDocument(doc_body)

    scanner = CommandScanner('wget', WgetExtractor())
    regions = scanner.scan(document)
    for r in regions:
        log_region(r, origin)
        try:
            exp = wget_explain(r.string)
        except InvalidCommandException as e:
            logging.error("Error processing wget command %s: %s", e.cmd, e.exception)
            continue
        document = wget_render(exp['url'], exp['opts'], exp['combo_exps'])
        explained_regions.append(package_region(r, document))

    return HttpResponse(json.dumps(explained_regions, indent=2))


@csrf_exempt
def explain(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    region_logger.info("Request for explanation for text from origin: %s", origin)

    error_template = get_template('error.html')

    try:
        exp = wget_explain(text)
    except InvalidCommandException as e:
        logging.error("Error processing wget command %s: %s", e.cmd, e.exception)
        error_html = error_template.render(Context({'text': text, 'type': 'wget command'}))
        return HttpResponse(error_html)
    else:
        exp_html = wget_render(exp['url'], exp['opts'], exp['combo_exps'])
        return HttpResponse(exp_html)
