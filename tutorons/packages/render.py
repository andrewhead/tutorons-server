#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.template.loader import get_template
from django.template import Context


logging.basicConfig(level=logging.INFO, format="%(message)s")


def render(package, header, explanation, url):
    package_template = get_template('package.html')
    context = {'package': package, 'hdr': header, 'exp': explanation, 'url': url}
    exp_html = package_template.render(Context(context))
    return exp_html
