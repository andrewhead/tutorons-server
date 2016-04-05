#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from tutorons.common.scanner import CommandScanner, InvalidCommandException
from tutorons.wget.explain import WgetExtractor, explain as wget_explain
from tutorons.wget.render import render as wget_render
from tutorons.common.dblogger import DbLogger
from tutorons.common.views import pagescan, snippetexplain


logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')
db_logger = DbLogger()


@csrf_exempt
@pagescan
def scan(html_doc):

    rendered_regions = []
    scanner = CommandScanner('wget', WgetExtractor())
    regions = scanner.scan(html_doc)
    for r in regions:
        try:
            exp = wget_explain(r.string)
        except InvalidCommandException as e:
            logging.error("Error processing wget command %s: %s", e.cmd, e.exception)
            continue
        document = wget_render(exp['url'], exp['opts'], exp['combo_exps'])
        rendered_regions.append((r, document))

    return rendered_regions


@csrf_exempt
@snippetexplain
def explain(text, edge_size):

    error_template = get_template('error.html')

    try:
        exp = wget_explain(text)
        document = wget_render(exp['url'], exp['opts'], exp['combo_exps'])
    except InvalidCommandException:
        document = error_template.render(Context({'text': text, 'type': 'wget command'}))
    return document
