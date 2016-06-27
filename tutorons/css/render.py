#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template.loader import get_template
from django.template import Context


logging.basicConfig(level=logging.INFO, format="%(message)s")


def render(explanations, examples):
    css_template = get_template('css.html')
    context = {
        'explanations': explanations,
        'examples': examples,
    }
    exp_html = css_template.render(Context(context))
    return exp_html
