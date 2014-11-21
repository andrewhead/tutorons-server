#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import json


def main(jsonFile):
    data = json.load(open(jsonFile))
    for answer in data:
        print "=== ANSWER ==="
        print "Id: " + str(answer['id_'])
        for line in answer['lines']:
            print line['type_'] + ": " + line['text'] + ", " + str(line['references'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split and print out StackOverflow answers")
    parser.add_argument("answer_file", help="JSON formatted answers from StackOverflow")
    args = parser.parse_args()
    answers = main(args.answer_file)
