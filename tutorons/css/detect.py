#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


def find_jquery_selector(string, edge_size):
    '''
    This routine attempts to find a Javascript string that is the closest to a user's original
    selection, where the original selection is contained within the string, but with additional
    context on each side 'edge_size' big.
    edge_size must be > 1 for this method to work properly.
    Returns the original selection (without context) if no Javascript string was found

    To find the string closest to the user's selection, it does the following:
    1. Finds all pairs of quotation marks (single or double quotes)
    2. Picks the pair of quotation marks closest to the user's original selection
    3. Returns the string encapsulated within those quotation marks
    '''
    # The ideal quotation position would be directly outside the user's original selection
    # (i.e., the first character of the edge right outside the original string)
    target = [edge_size - 1, len(string) - edge_size]
    quote_pairs = []
    double_quote = None
    single_quote = None

    # Discover all pairs of quotation marks
    for i, c in enumerate(string):
        if c == "'":
            if single_quote is not None:
                quote_pairs.append((single_quote, i))
            single_quote = i
        elif c == '"':
            if double_quote is not None:
                quote_pairs.append((double_quote, i))
            double_quote = i

    # If there are no quotation pairs, then return the original string
    if len(quote_pairs) == 0:
        return string[edge_size:len(string) - edge_size]

    # Detect the pair of quotes closest to the original region
    dist = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
    distances = {qp: dist(qp, target) for qp in quote_pairs}
    best = min(distances.items(), key=lambda item: item[1])
    best_qp = best[0]
    return string[best_qp[0] + 1:best_qp[1]]
