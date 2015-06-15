#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_descendants(x):
    ''' Get all descendants of an object. '''

    if isinstance(x, list):
        return [i for el in x for i in get_descendants(el)]
    elif hasattr(x, '__dict__'):
        return [x] + [i for child in x.__dict__.values() for i in get_descendants(child)]
    elif isinstance(x, dict):
        return [i for child in x for i in get_descendants(child)]
    else:
        return []
