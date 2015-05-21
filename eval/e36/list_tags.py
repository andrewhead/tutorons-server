#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import argparse


logging.basicConfig(level=logging.INFO, format="%(message)s")


def read_entries(file_):
    entries = []
    with open(file_) as infile:
        for l in infile.readlines()[1:]:
            tokens = l.split(',')
            post_id = int(tokens[0][1:-1])
            tags = tokens[1][2:-4].split('><')
            for t in tags:
                entries.append((post_id, t))
    return entries


def print_entries(entries):
    print 'Post ID,tag'
    for e in entries:
        print ','.join(str(_) for _ in [e[0], e[1], ''])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()
    entries = read_entries(args.infile)
    print_entries(entries)
