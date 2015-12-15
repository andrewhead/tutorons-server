#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template.loader import get_template
from django.template import Context


logging.basicConfig(level=logging.INFO, format="%(message)s")

# TODO get rid of selector stuff, add in built in explanation, 
# TODO add support for arguments and examples, how to actually evaluate the expression
# TODO need some tweaking of html template?

def render(explanation):
    python_template = get_template('python.html')
    context = {'exp': explanation,}
    exp_html = python_template.render(Context(context))
    return exp_html
