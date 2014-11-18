#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import json
from bs4 import BeautifulSoup
import re


def main(answerFile):
    answers = json.load(open(answerFile))
    for answer in answers['items']:
        soup = BeautifulSoup(answer['body'])
        print "=====Answer " + str(answer['answer_id']) + "====="
        children = [child for child in soup.children if child != '\n']
        for child in children:
            if child.name == 'p':
                print "==Text=="
                print child.text.rstrip()
                codeSnippets = child.findAll('code')
                if codeSnippets:
                    print "=Inline Code="
                    for snippet in codeSnippets:
                        print snippet.text
            elif child.name == 'pre':
                print "==Code Block=="
                print child.text.rstrip()
                print "=Short Comments="
                for line in child.text.rstrip().split('\n'):
                    if re.match('.*//.*', line):
                        print line
                print "=Long Comments="
                state = "neutral"
                commentString = []
                for line in child.text.rstrip().split('\n'):
                    if state == "neutral" and re.match('.*/\*.*', line):
                        state = "open comment"
                    if state == "open comment":
                        commentString.append(line)
                        if re.match('.*\*/.*', line):
                            state = "neutral"
                            print '\n'.join(commentString)
                            commentString = []
        print "\n\n"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split and print out StackOverflow answers")
    parser.add_argument("answer_file", help="JSON formatted answers from StackOverflow")
    args = parser.parse_args()
    main(args.answer_file)
