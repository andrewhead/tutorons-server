#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from py4j.java_gateway import JavaGateway
from cssselect.parser import Element, SelectorSyntaxError
import cssselect
import re
from bs4 import BeautifulSoup
import tinycss


logging.basicConfig(level=logging.INFO, format="%(message)s")

''' Our CSS explainer is implemented in Java, so we open up a gateway through Py4J for now. '''
gateway = JavaGateway()
explainer = gateway.entry_point.getExplainer()


def explain(selector):
    return explainer.explain(selector)