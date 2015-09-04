#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

from tutorons.common.htmltools import HtmlDocument
from tutorons.common.util import log_region
from tutorons.common.scanner import NodeScanner, CommandScanner, InvalidCommandException
from tutorons.wget.explain import WgetExtractor, explain as wget_explain
from tutorons.css.detect import find_jquery_selector
from tutorons.css.explain import CssSelectorExtractor, explain as css_explain, is_selector
from parsers.css.examples.examplegen import get_example as css_example
from tutorons.regex.extract import GrepRegexExtractor, SedRegexExtractor, JavascriptRegexExtractor,\
    ApacheConfigRegexExtractor
from tutorons.regex.explain import InvalidRegexException, visualize as regex_viz
from tutorons.regex.examples import urtext


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')


def home(request):
    return render(request, 'home.html', {})


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
def explain_wget(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    region_logger.info("Request for explanation for text from origin: %s", origin)

    wget_template = get_template('wget.html')
    error_template = get_template('error.html')

    try:
        exp = wget_explain(text)
    except InvalidCommandException as e:
        logging.error("Error processing wget command %s: %s", e.cmd, e.exception)
        error_html = error_template.render(Context({'text': text, 'type': 'wget command'}))
        return HttpResponse(error_html)
    else:
        exp_html = wget_template.render(Context(exp))
        return HttpResponse(exp_html)


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


@csrf_exempt
def explain_css(request):

    text = request.POST.get('text')
    edge_size = int(request.POST.get('edge_size', 0))
    origin = request.POST.get('origin')
    region_logger.info("Request for text from origin: %s", origin)

    css_template = get_template('css.html')
    error_template = get_template('error.html')

    if edge_size > 0:
        text = find_jquery_selector(text, edge_size)

    if is_selector(text):
        ctx = {}
        ctx['exp'] = css_explain(text)
        ctx['example'] = css_example(text)
        exp_html = css_template.render(Context(ctx))
        return HttpResponse(exp_html)
    else:
        logging.error("Error processing CSS selector %s", text)
        error_html = error_template.render(Context({'text': text, 'type': 'CSS selector'}))
        return HttpResponse(error_html)


@csrf_exempt
def regex(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    results = {}
    document = HtmlDocument(doc_body)
    regex_template = get_template('regex.html')
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
            ctx = {}
            log_region(r, origin)

            try:
                ctx['svg'] = regex_viz(r.pattern)
            except InvalidRegexException as e:
                logging.error("Error processing regex %s: %s", r.pattern, e)

            try:
                ctx['example'] = urtext(r.pattern)
            except Exception as e:
                logging.error("Error processing regex %s: %s", r.pattern, e)

            if len(ctx) == 0:
                continue

            exp_html = regex_template.render(Context(ctx))
            results[r.string] = exp_html

    return HttpResponse(json.dumps(results, indent=2))


@csrf_exempt
def explain_regex(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    region_logger.info("Request for text from origin: %s", origin)

    regex_template = get_template('regex.html')
    error_template = get_template('error.html')

    try:
        svg = regex_viz(text)
    except InvalidRegexException as e:
        logging.error("Error processing regular expression %s: %s", e.pattern, e.msg)
        error_html = error_template.render(Context({'text': text, 'type': 'regular expression'}))
        return HttpResponse(error_html)
    else:
        ctx = {'svg': svg}
        exp_html = regex_template.render(Context(ctx))
        return HttpResponse(exp_html)
