#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import argparse
import re
import sys
from cStringIO import StringIO
from enum import Enum


from tutorons.regex.tree import PatternTree
from tutorons.regex.nodes import Node, LiteralNode, RangeNode, InNode, RepeatNode, ChoiceNode,\
    GroupNode, NegateNode, CategoryNode, AnyNode, BranchNode


logging.basicConfig(level=logging.INFO, format="%(message)s")


class LineType(Enum):
    IN = "^in$"
    BRANCH = "^branch$"
    OR = "^or$"
    ROOT = "^$"
    LITERAL = "^literal"
    REPEAT = "^max_repeat"
    SUBPATTERN = "^subpattern"
    RANGE = "^range"
    NEGATE = "^negate"
    CATEGORY = "^category"
    ANY = "^any"

    @staticmethod
    def getLineType(string):
        for lt in LineType:
            if re.match(lt.value, string):
                return lt
        return None


def capture_stdout(func):

    def _outer(*args, **kwargs):
        orig_stdout = sys.stdout
        stdout_buffer = StringIO()
        sys.stdout = stdout_buffer
        func(*args, **kwargs)
        sys.stdout = orig_stdout
        return stdout_buffer.getvalue()

    return _outer


@capture_stdout
def describe_regex(regex):
    re.purge()
    re.compile(regex, re.DEBUG)


def _count_indents(line):
    return len(re.findall("^\s*", line)[0]) / 2


''' Methods for parsing lines into node data. '''
parse_literal = lambda line: int(re.match('^literal (\d+)', line).group(1))
parse_category = lambda line: re.match('^category category_(\w+)', line).group(1)


def parse_repeat(line):
    bounds = [int(_) for _ in re.match('^max_repeat (\d+) (\d+)', line).groups()]
    ranged = not (bounds[0] == bounds[1])
    min_repeats = bounds[0]
    max_repeats = bounds[1]
    return (ranged, min_repeats, max_repeats)


def parse_range(line):
    match = re.match('^range \((\d+), (\d+)\)', line)
    return int(match.group(1)), int(match.group(2))


def getnode(line):
    line_type = LineType.getLineType(line.strip())
    if line_type == LineType.LITERAL:
        node = LiteralNode(parse_literal(line), line)
    elif line_type == LineType.RANGE:
        r = parse_range(line)
        node = RangeNode(r[0], r[1], line)
    elif line_type == LineType.IN:
        node = InNode(line)
    elif line_type == LineType.REPEAT:
        ranged, minr, maxr = parse_repeat(line.strip())
        node = RepeatNode(ranged, minr, maxr, line)
    elif line_type == LineType.BRANCH:
        node = ChoiceNode(line)
    elif line_type == LineType.OR:
        node = ChoiceNode(line)
    elif line_type == LineType.SUBPATTERN:
        node = GroupNode(line)
    elif line_type == LineType.NEGATE:
        node = NegateNode(line)
    elif line_type == LineType.CATEGORY:
        node = CategoryNode(parse_category(line), line)
    elif line_type == LineType.ANY:
        node = AnyNode(line)
    else:
        node = Node(line)
    return node


def get_brothers(lines):
    indexes = [i for i, l in enumerate(lines) if _count_indents(l) == 0]
    brothers = []
    for i in range(0, len(indexes) - 1):
        cr, nx = indexes[i], indexes[i+1]
        brothers.append('\n'.join(lines[cr:nx]))
    if len(lines) > 1:
        brothers.append('\n'.join(lines[indexes[-1]:]))
    elif len(lines) == 1 and lines[0].strip() != '':
        brothers.append(lines[0])
    return brothers


def get_child_text(lines):
    clines = [re.sub('^\s\s', '', l) for l in lines[1:]]
    return '\n'.join(clines)


def are_brothers_branches(brothers):
    if len(brothers) == 0:
        return False
    else:
        first_brother = brothers[0]
        blines = first_brother.split('\n')
        return (LineType.getLineType(blines[0]) == LineType.BRANCH)


def parse_text(text):
    lines = text.strip().split('\n')
    brothers = get_brothers(lines)
    nodes = []
    for btext in brothers:
        blines = btext.split('\n')
        bnode = getnode(blines[0])
        if len(blines) > 0:
            ctext = get_child_text(blines)
            bnode.children.extend(parse_text(ctext))
        nodes.append(bnode)
    if are_brothers_branches(brothers):
        choice_nodes = nodes
        branch_node = BranchNode(lines[0])
        branch_node.children.extend(choice_nodes)
        nodes = [branch_node]
    return nodes


def parse_regex(regex):
    ''' Parse a regular expression into a tree. '''
    description = describe_regex(regex)
    first_children = parse_text(description)
    root = Node("ROOT")
    root.children = first_children
    return PatternTree(root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Give examples of when a regular expression is satisfied or not.')
    parser.add_argument('regex', help="regular expression")
    args = parser.parse_args()
    tree = parse_regex(args.regex)
    print tree
