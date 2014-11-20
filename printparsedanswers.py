#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import json


def main():
    data = json.load(open('data/309424.answers_processed.json'))
    for answer in data:
        print "=== ANSWER ==="
        print "Id: " + str(answer['id_'])
        for line in answer['lines']:
            print line['type_'] + ": " + line['text'] + ", " + str(line['references'])


if __name__ == '__main__':
    main()

