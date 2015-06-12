#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_css_selector(tag):
    ''' Create a CSS selector that can choose this tag from the document. '''

    elements = []

    element = tag
    while element.name != '[document]':

        parent = element.parent
        type_siblings = parent.find_all(element.name, recursive=False)
        index = -1
        for i, s in enumerate(type_siblings):
            if id(s) == id(element):
                index = i + 1  # in CSS, nth-of-type index starts at 1
                break

        elements.insert(0, {'name': element.name, 'index': index})
        element = parent

    selector = ' > '.join([
        '%s:nth-of-type(%d)' % (el['name'], el['index'])
        for el in elements])
    return selector
