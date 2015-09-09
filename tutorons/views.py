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

from tutorons.common.htmltools import HtmlDocument, get_css_selector
from tutorons.common.util import log_region
from tutorons.common.scanner import NodeScanner, CommandScanner, InvalidCommandException
from tutorons.wget.explain import WgetExtractor, explain as wget_explain
from tutorons.wget.render import render as wget_render
from tutorons.css.detect import find_jquery_selector
from tutorons.css.explain import CssSelectorExtractor, explain as css_explain, is_selector
from tutorons.css.render import render as css_render
from parsers.css.examples.examplegen import get_example as css_example
from tutorons.regex.extract import GrepRegexExtractor, SedRegexExtractor, JavascriptRegexExtractor,\
    ApacheConfigRegexExtractor
from tutorons.regex.explain import InvalidRegexException, visualize as regex_viz
from tutorons.regex.examples import urtext
from tutorons.regex.render import render as regex_render


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')


def home(request):
    return render(request, 'home.html', {})


def package_region(region, document):
    return {
        'node': get_css_selector(region.node),
        'start_index': region.start_offset,
        'end_index': region.end_offset,
        'document': document,
    }


@csrf_exempt
def wget(request):

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
def explain_wget(request):

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


@csrf_exempt
def css(request):

    doc_body = request.POST.get('document')
    origin = request.POST.get('origin')
    region_logger.info("Request for page from origin: %s", origin)

    explained_regions = []
    document = HtmlDocument(doc_body)
    extractor = CssSelectorExtractor()

    scanner = NodeScanner(extractor, ['code', 'pre'])
    regions = scanner.scan(document)
    for r in regions:
        log_region(r, origin)
        exp = css_explain(r.string)
        example = css_example(r.string)
        document = css_render(exp, example)
        explained_regions.append(package_region(r, document))

    return HttpResponse(json.dumps(explained_regions, indent=2))


@csrf_exempt
def explain_css(request):

    text = request.POST.get('text')
    edge_size = int(request.POST.get('edge_size', 0))
    origin = request.POST.get('origin')
    region_logger.info("Request for text from origin: %s", origin)

    error_template = get_template('error.html')

    if edge_size > 0:
        text = find_jquery_selector(text, edge_size)

    if is_selector(text):
        exp = css_explain(text)
        example = css_example(text)
        exp_html = css_render(exp, example)
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

    explained_regions = []
    document = HtmlDocument(doc_body)
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

            try:
                svg = regex_viz(r.pattern)
            except InvalidRegexException as e:
                logging.error("Error processing regex %s: %s", r.pattern, e)
                svg = None

            try:
                example = urtext(r.pattern)
            except Exception as e:
                logging.error("Error processing regex %s: %s", r.pattern, e)
                example = None

            if example is not None or svg is not None:
                document = regex_render(svg, example)
                explained_regions.append(package_region(r, document))

    return HttpResponse(json.dumps(explained_regions, indent=2))


@csrf_exempt
def explain_regex(request):

    text = request.POST.get('text')
    origin = request.POST.get('origin')
    region_logger.info("Request for text from origin: %s", origin)

    try:
        svg = regex_viz(text)
        html = regex_render(svg)
    except InvalidRegexException as e:
        logging.error("Error processing regular expression %s: %s", e.pattern, e.msg)
        error_template = get_template('error.html')
        html = error_template.render(Context({'text': text, 'type': 'regular expression'}))

    return HttpResponse(html)
