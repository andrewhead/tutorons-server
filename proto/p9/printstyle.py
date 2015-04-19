#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from enum import Enum
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


class PrintStyle(Enum):
    ''' Stylings for formatting ASCII output to STDOUT. '''
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

END_STYLE = '\033[0m'  # For clearing formatting


def main():
    for s in PrintStyle:
        print s.value + "Hello" + END_STYLE


if __name__ == '__main__':
    main()

