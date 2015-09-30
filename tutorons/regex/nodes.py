#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re


logging.basicConfig(level=logging.INFO, format="%(message)s")


class Node(object):

    def __init__(self, text=''):
        self.children = []
        self.text = text

    def __str__(self):
        string = ""
        string += "(" + str(self.__class__) + ": " + self.text
        if len(self.children) > 0:
            string += "\n"
        for c in self.children:
            cstring = re.sub('^(?=[^$])', '  ', str(c), flags=re.MULTILINE)
            string += cstring
        string += ')\n'
        return string


class LiteralNode(Node):

    def __init__(self, value, *args, **kwargs):
        super(LiteralNode, self).__init__(*args, **kwargs)
        self.value = value


class CategoryNode(Node):

    def __init__(self, classname, *args, **kwargs):
        super(CategoryNode, self).__init__(*args, **kwargs)
        self.classname = classname


class AnyNode(Node):
    pass


class RangeNode(Node):

    def __init__(self, lo, hi, *args, **kwargs):
        super(RangeNode, self).__init__(*args, **kwargs)
        self.lo = lo
        self.hi = hi


class NegateNode(Node):
    pass


class InNode(Node):

    @property
    def negated(self):
        for ch in self.children:
            if isinstance(ch, NegateNode):
                return True
        return False


class BranchNode(Node):

    def __init__(self, *args, **kwargs):
        super(BranchNode, self).__init__(*args, **kwargs)
        self.choice = None


class ChoiceNode(Node):
    pass


class GroupNode(Node):
    pass


class RepeatNode(Node):

    def __init__(self, ranged, min_repeat, max_repeat, *args, **kwargs):
        super(RepeatNode, self).__init__(*args, **kwargs)
        self.min_repeat = min_repeat
        self.max_repeat = max_repeat
        self.ranged = ranged
        self.repetitions = None
