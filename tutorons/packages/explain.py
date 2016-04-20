#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from packages import explanations

logging.basicConfig(level=logging.INFO, format="%(message)s")


def explain(package):
    return explanations[package]
