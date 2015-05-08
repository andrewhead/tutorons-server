#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as Soup
import json

from tutorons.wget.explain import explain as wget_explain
from tutorons.wget.explain import detect as wget_detect


logging.basicConfig(level=logging.INFO, format="%(message)s")


@csrf_exempt
def wget(request):
    
    results = {}
    soup = Soup(request.body)
    wget_template = get_template('wget.html')

    for block in soup.find_all('code'):
        snippet = block.text

        for line in snippet.split('\n'):
            line_clean = line.strip()

            if wget_detect(line_clean):
                exp = wget_explain(line_clean)
                exp_html = wget_template.render(Context(exp))
                results[line_clean] = exp_html

    # print json.dumps(results, indent=2)
    return HttpResponse(json.dumps(results, indent=2))
