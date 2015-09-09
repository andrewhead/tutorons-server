#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template import Context
from django.template.loader import get_template


logging.basicConfig(level=logging.INFO, format="%(message)s")


def render(url, options=None, optcombos=None):
    options = [] if options is None else options
    optcombos = [] if optcombos is None else optcombos
    template = get_template('wget.html')
    context = {
        'url': url,
        'opts': options,
        'combo_exps': optcombos,
    }
    return template.render(Context(context))
