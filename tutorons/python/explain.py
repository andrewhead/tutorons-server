#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def filter_non_ascii(c):
    if ord(c) > 127:
        return ' '
    return c

def explain(builtin):
    return explanations[builtin]

def generate_explanation_dict():
    functions = open('tutorons/python/functions.txt', 'r')
    # functions = open('functions.txt', 'r')

    built_in_dict = {}
    line = functions.readline()
    curr_built_in = None
    builtins = ['__import__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer', 'bytearray', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile', 'file', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'long', 'map', 'max', 'memoryview', 'min', 'next', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']

    while line:
        # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position 46: ordinal not in range(128)
        orig_line = line
        line = ''.join(map(filter_non_ascii, line))
        # print 'line: '  + line
        if orig_line == '\n':
            print "require newline"
        if 'class ' in line:
            builtin = line[(line.find('class ') + 6):line.find('(')] 
        else:
            builtin = line[:line.find('(')]
        # next built in
        if builtin in builtins and builtin != curr_built_in:
            built_in_dict[builtin] = line
            curr_built_in = builtin
        #just add to the last entry in the dict
        else: 
            if curr_built_in:
                built_in_dict[curr_built_in] += line
                if orig_line == '\n':
                    built_in_dict[curr_built_in] += '\n'
        line = functions.readline()
    # print built_in_dict
    print built_in_dict['oct']
    return built_in_dict

explanations = generate_explanation_dict()
