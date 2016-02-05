#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from builtins import explanations

logging.basicConfig(level=logging.INFO, format="%(message)s")


def explain(builtin):
    return explanations[builtin]
