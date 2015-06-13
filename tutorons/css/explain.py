#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from py4j.java_gateway import JavaGateway
from slimit.lexer import Lexer
from cssselect.parser import Element, SelectorSyntaxError
import cssselect
import re

from tutorons.css.tags import HTML_TAGS


logging.basicConfig(level=logging.INFO, format="%(message)s")

''' Our CSS explainer is implemented in Java, so we open up a gateway through Py4J for now. '''
gateway = JavaGateway()
explainer = gateway.entry_point.getExplainer()


def extract_strings(jscode):

    lexer = Lexer()
    lexer.input(jscode)

    strings = []
    while True:
        try:
            tok = lexer.token()
            if not tok:
                break
            if tok.type == "STRING":
                strings.append(tok.value[1:-1])
        except TypeError:
            break

    return strings


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


def is_selector(string):
    ''' Check to see if string represents valid HTML selector. '''
    try:
        # cssselect doesn't like links, so we replace them.
        string = re.sub(r"(href.=)([^\]]*)\]", r"\1fakelink]", string)
        tree = cssselect.parse(string)
        selector_parts = get_descendants(tree)
        for part in selector_parts:
            if isinstance(part, Element):
                if part.element not in HTML_TAGS:
                    return False
        return True
    except SelectorSyntaxError:
        return False


def detect(jscode):
    strings = extract_strings(jscode)
    sels = [s for s in strings if is_selector(s)]
    return sels


def explain(selector):
    return explainer.explain(selector)
