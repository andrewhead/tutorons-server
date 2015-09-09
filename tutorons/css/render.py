#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template.loader import get_template
from django.template import Context


logging.basicConfig(level=logging.INFO, format="%(message)s")


def render(explanation, example):
    css_template = get_template('css.html')
    context = {
        'exp': explanation,
        'example': example,
    }
    exp_html = css_template.render(Context(context))
    return exp_html
