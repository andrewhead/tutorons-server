#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import os
import argparse
from nltk.parse import stanford
from enum import Enum


logging.basicConfig(level=logging.INFO, format="%(message)s")

''' Requirement: Stanford parser jars installed at this location. '''
SP_PATH = os.path.join(os.pardir, os.pardir, 'deps')
os.environ['STANFORD_PARSER'] = SP_PATH
os.environ['STANFORD_MODELS'] = SP_PATH
parser = stanford.StanfordParser(model_path=os.path.join(SP_PATH, 'englishPCFG.ser.gz'))


class RootType(Enum):
    NOUN = 1
    VERB = 2
    UNKNOWN = 3


def get_tree_root_type(tree):
    for token, tag in tree.pos():
        if tag.startswith('N'):
            return RootType.NOUN
        elif tag.startswith('V'):
            return RootType.VERB
    return RootType.UNKNOWN


def get_root_type(phrase):
    trees = parser.raw_parse(phrase)
    tree = [_ for _ in trees][0]
    return get_tree_root_type(tree)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get root type of phrase.")
    parser.add_argument('phrase', help="English phrase to parse")
    args = parser.parse_args()
    print get_root_type(args.phrase)
