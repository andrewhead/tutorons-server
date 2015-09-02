#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import json
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from tutorons.common.htmltools import HtmlDocument
from tutorons.common.util import log_region
from tutorons.common.scanner import NodeScanner, CommandScanner, InvalidCommandException
from tutorons.wget.explain import WgetExtractor, explain as wget_explain
from tutorons.css.explain import CssSelectorExtractor, explain as css_explain
from tutorons.regex.extract import GrepRegexExtractor, SedRegexExtractor, JavascriptRegexExtractor,\
    ApacheConfigRegexExtractor
from parsers.css.examples.examplegen import get_example as css_example


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')


def home(request):
    return render(request, 'home.html', {})


@csrf_exempt
def regex(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    results = {}
    document = HtmlDocument(doc_body)
    css_template = get_template('regex.html')
    extractors = [
        GrepRegexExtractor(),
        SedRegexExtractor(),
        JavascriptRegexExtractor(),
        ApacheConfigRegexExtractor(),
    ]

    for extractor in extractors:
        scanner = NodeScanner(extractor, ['code', 'pre'])
        regions = scanner.scan(document)
        for r in regions:
            log_region(r, origin)
            pattern = r.pattern.replace('/', r'\/')  # Regexper requires forward-slashes are escaped
            res = requests.get(settings.REGEX_SVG_ENDPOINT, params={'pattern': pattern})
            soup = BeautifulSoup(res.content)
            svg = str(soup.svg)
            ctx = {'svg': svg}
            exp_html = css_template.render(Context(ctx))
            results[r.string] = exp_html

    return HttpResponse(json.dumps(results, indent=2))


@csrf_exempt
def wget(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    results = {}
    document = HtmlDocument(doc_body)
    wget_template = get_template('wget.html')

    scanner = CommandScanner('wget', WgetExtractor())
    regions = scanner.scan(document)
    for r in regions:
        log_region(r, origin)
        try:
            exp = wget_explain(r.string)
        except InvalidCommandException as e:
            logging.error("Error processing wget command %s: %s", e.cmd, e.exception)
            continue
        exp_html = wget_template.render(Context(exp))
        results[r.string] = exp_html

    return HttpResponse(json.dumps(results, indent=2))


@csrf_exempt
def css(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    results = {}
    ctx = {}
    document = HtmlDocument(doc_body)
    css_template = get_template('css.html')
    extractor = CssSelectorExtractor()

    scanner = NodeScanner(extractor, ['code', 'pre'])
    regions = scanner.scan(document)
    for r in regions:
        log_region(r, origin)
        ctx['exp'] = css_explain(r.string)
        ctx['example'] = css_example(r.string)
        exp_html = css_template.render(Context(ctx))
        results[r.string] = exp_html

    return HttpResponse(json.dumps(results, indent=2))
