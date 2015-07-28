#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as Soup
import json

from tutorons.common.node_detector import CommandNodeDetector
from tutorons.wget.explain import WgetExtractor, explain as wget_explain
from tutorons.css.explain import CssSelectorExtractor, explain as css_explain
from parsers.css.examples.examplegen import get_example as css_example


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')


def home(request):
    return render(request, 'home.html', {})


@csrf_exempt
def wget(request):

    document = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    results = {}
    soup = Soup(document)
    wget_template = get_template('wget.html')

    node_detector = CommandNodeDetector('wget')
    nodes = node_detector.detect(soup)

    extractor = WgetExtractor()
    for block in nodes:
        regions = extractor.extract(block)
        for r in regions:
            exp = wget_explain(r.string)
            exp_html = wget_template.render(Context(exp))
            results[r.string] = exp_html

    return HttpResponse(json.dumps(results, indent=2))


@csrf_exempt
def css(request):

    document = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    results = {}
    ctx = {}
    soup = Soup(document)
    css_template = get_template('css.html')
    extractor = CssSelectorExtractor()

    for block in soup.find_all('code') + soup.find_all('pre'):
        regions = extractor.extract(block)
        for r in regions:
            ctx['exp'] = css_explain(r.string)
            ctx['example'] = css_example(r.string)
            exp_html = css_template.render(Context(ctx))
            results[r.string] = exp_html

    return HttpResponse(json.dumps(results, indent=2))
