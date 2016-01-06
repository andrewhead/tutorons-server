#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from bs4 import BeautifulSoup
import collections

logging.basicConfig(level=logging.INFO, format="%(message)s")

fcns = open('tutorons/python/fcns.txt', 'r').read()
builtin_doc = BeautifulSoup(fcns)
dt = builtin_doc.findAll('dt')  # headers
dd = builtin_doc.findAll('dd')  # explanations
explanations = collections.OrderedDict()  # builtin : explanation (dt, dd)


def resolve(a):
    """Resolve relative hyperlinks to poin to python docs instead of current page"""
    if a['href'][0] == '#':
        a['href'] = a['href'].replace(
            a['href'],
            'https://docs.python.org/2/library/functions.html' + a['href'])
    else:
        a['href'] = a['href'].replace(a['href'], 'https://docs.python.org/2/library/' + a['href'])

# fix all relative hyperlinks
for tag in dd + dt:
    map(resolve, tag.findAll('a'))

# group dt tags for the same builtin and add to explanations dict
for tag in dt:
    if tag.code.text.encode() not in explanations:
        explanations[tag.code.text.encode()] = tag
    else:
        explanations[tag.code.text.encode()].append(tag)

# add descriptions to explanations dict
for builtin, desc in zip(explanations, dd):
    explanations[builtin] = (str(explanations[builtin]), str(desc))


def explain(builtin):
    return explanations[builtin]
