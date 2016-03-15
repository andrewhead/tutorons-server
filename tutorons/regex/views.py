#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from tutorons.common.scanner import NodeScanner
from tutorons.regex.extract import GrepRegexExtractor, SedRegexExtractor, JavascriptRegexExtractor,\
    ApacheConfigRegexExtractor
from tutorons.regex.explain import InvalidRegexException, visualize as regex_viz
from tutorons.regex.examples import get_examples
from tutorons.regex.render import render as regex_render
from tutorons.common.dblogger import DBLogger
from tutorons.common.views import pagescan, snippetexplain


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DBLogger()


@csrf_exempt
@pagescan
def scan(html_doc):

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
                rendered_regions.append((r, document))
    return rendered_regions


@csrf_exempt
@snippetexplain
def explain(text, edge_size):

    try:
        svg = regex_viz(text)
        explanation = regex_render(svg)
    except InvalidRegexException:
        error_template = get_template('error.html')
        explanation = error_template.render(Context({'text': text, 'type': 'regular expression'}))

    return explanation
