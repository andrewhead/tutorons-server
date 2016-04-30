#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re
import string

from tutorons.common.extractor import Region
from tutorons.packages.packages import explanations

logging.basicConfig(level=logging.INFO, format="%(message)s")


class PackageExtractor(object):

    def extract(self, node):
        text = node.text.encode('ascii', 'ignore')
        regions = []
        char_index = 0
        for line in text.split('\n'):
            words = re.findall(r"\b[^\W\d_]+-?'?[^\W\d_]+\b", line)

            for word in words:
                if word in explanations.keys(): # Picked up on a package name
                    first_char = char_index + string.index(line, word)
                    last_char = char_index + string.index(line, word) + len(word) - 1
                    r = Region(node, first_char, last_char, word)
                    regions.append(r)
                    char_index += (len(line) + 1)  # every line has at least 1 char: the newline

        return regions
