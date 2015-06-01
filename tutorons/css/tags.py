#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")

''' We include None in this list because patterns that match all tags
    (e.g. ".klazz") yield an Element with property 'element' == None. '''
HTML_TAGS = ['a', 'abbr', 'address', 'area', 'article', 'aside', 
    'audio', 'b', 'base', 'bb', 'bdo', 'blockquote', 'body', 
    'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 
    'colgroup', 'command', 'datagrid', 'datalist', 'dd', 'del', 
    'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed', 
    'fieldset', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 
    'h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 
    'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'map', 
    'mark', 'menu', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 
    'optgroup', 'option', 'output', 'p', 'param', 'pre', 'progress', 
    'q', 'rp', 'rt', 'ruby', 'samp', 'script', 'section', 'select', 
    'small', 'source', 'span', 'strong', 'style', 'sub', 'sup', 
    'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 
    'time', 'title', 'tr', 'ul', 'var', 'video', None,
]
