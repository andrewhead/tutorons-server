#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template import Context
from django.template.loader import get_template


logging.basicConfig(level=logging.INFO, format="%(message)s")


def render(pattern, visualization=None, examples=None):
    context = {
        'patt': pattern,
        'svg': visualization,
        'examples': examples,
    }
    template = get_template('regex.html')
    html = template.render(Context(context))
    return html
