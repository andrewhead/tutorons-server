#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template.loader import get_template
from django.template import Context


logging.basicConfig(level=logging.INFO, format="%(message)s")


def render(builtin, explanation, header):
    python_template = get_template('python.html')
    context = {'builtin': builtin, 'hdr': header, 'exp': explanation}
    exp_html = python_template.render(Context(context))
    return exp_html
