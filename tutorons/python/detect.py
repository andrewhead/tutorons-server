#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import ast

from tutorons.common.extractor import Region


logging.basicConfig(level=logging.INFO, format="%(message)s")

explanations = {"len" : "len_explain",
                "abs" : "abs_explain",
                "bin" : "bin_explain", 
                "all" : "all_explain", }
 
def filter_non_ascii(c):
    if ord(c) > 127:
        return ' '
    return c

def findOffset(text_list, call):
    """Takes in a text as a list and a call and finds the start of call within text"""
    offset = 0
    if call.lineno > 1:
        for l in xrange(call.lineno - 1):
            # add 1 to account for newline characters
            offset += len(text_list[l]) + 1
    offset += call.col_offset
    # print offset
    return offset

def findBuiltIns(ast_object):
    """Takes in an ast_object and recursively checks for builtin-ins, returns a list of all builtins in the ast_object"""
    rtn = []
    #turn into a case switch
    # print ast_object
    if isinstance(ast_object, ast.Expr):
        ast_object = ast_object.value
    if isinstance(ast_object, ast.Num):
        return rtn
    elif isinstance(ast_object, ast.Call):
        if ast_object.func.id in explanations:
            rtn += [ast_object]
        #flatten this into a list comprehension
        for arg in ast_object.args:
            # print "in here"
            rtn += findBuiltIns(arg)
        # print rtn 
        return rtn
    elif isinstance(ast_object, ast.BinOp):
        return findBuiltIns(ast_object.left) + findBuiltIns(ast_object.right)
    elif isinstance(ast_object, ast.Assign) or isinstance(ast_object, ast.AugAssign):
        return findBuiltIns(ast_object.value)
    elif isinstance(ast_object, ast.Print):
        for value in ast_object.values:
            rtn += findBuiltIns(value) 
        return rtn
    else:
        # print rtn
        return rtn

class PythonBuiltInExtractor(object):
    #TODO:  recurse down binary operations checking left & right for calls
    #       recurse down a call's args
    def extract(self, node):
        text = ''.join(map(filter_non_ascii, node.text))
        print "...................................\n" + text + "\n"
        text_list = text.split('\n')
        offset = 0
        valid_regions = []

        calls = []
        try:
            ast_objects = ast.parse(text).body
        except:
            ast_objects = []
        print "ast_objects: " + str(ast_objects)
        for ast_object in ast_objects:
            calls += findBuiltIns(ast_object)

        # package call objects into regions
        for call in calls:
            built_in = call.func.id
            start = findOffset(text_list, call)
            valid_regions.append(Region(node, start, start + len(built_in) - 1, built_in))
        print "valid_regions: " + str(valid_regions)
        return valid_regions