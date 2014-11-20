#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from enum import Enum
import argparse
import json
import jsonpickle
from bs4 import BeautifulSoup
import re


class Answer(object):

    def __init__(self, id_):
        self.id_ = id_
        self.lines = []
 
    def append(self, line):
        self.lines.append(line)


class Line(object):

    def __init__(self, text, type_):
        self.text = text
        self.type_ = type_
        self.references = []

    def addReference(self, reference):
        self.references.append(reference)


class LineType(Enum):
    TEXT = "text",
    CODE = "code",
    CODE_COMMENT_INLINE = "codecommentinline",
    CODE_COMMENT_LONG = "codecommentlong",

    def __getstate__(self):
        ''' When converting to JSON, return the associated string. '''
        return self.value[0]


class CommentState(Enum):
    OPEN = "open",
    CLOSED = "closed",


def parseAnswers(answerFile):

    answerData = json.load(open(answerFile))
    answers = []
    for item in answerData['items']:

        ''' Create answer. '''
        answer = Answer(item['answer_id'])

        ''' Parse the answer to separate lines. '''
        soup = BeautifulSoup(item['body'])
        tags = [tag for tag in soup.children if tag != '\n']
        for tag in tags:
            if tag.name == 'p':
                ''' Process text blocks. '''
                for sentence in tag.decode_contents().split('.\s'):
                    if sentence == "":
                        continue
                    sentenceSoup = BeautifulSoup(sentence)
                    line = Line(sentenceSoup.text, LineType.TEXT)
                    ''' Look for inline references to variable and class names. '''
                    references = sentenceSoup.findAll('code')
                    for ref in references:
                        line.addReference(ref.text)
                    answer.append(line)
            elif tag.name == 'pre':
                ''' Process code blocks. '''
                commentState = CommentState.CLOSED
                for line in tag.text.rstrip().split('\n'):
                    ''' Check for comment start. '''
                    if commentState == CommentState.CLOSED and re.match('.*/\*.*', line):
                        commentState = CommentState.OPEN
                    ''' Capture comments. '''
                    if commentState == CommentState.OPEN:
                        answer.append(Line(line, LineType.CODE_COMMENT_LONG))
                        if re.match('.*\*/.*', line):
                            commentState = CommentState.CLOSED
                    elif commentState == CommentState.CLOSED and re.match('.*//.*', line):
                        answer.append(Line(line, LineType.CODE_COMMENT_INLINE))
                    else:
                        answer.append(Line(line, LineType.CODE))
    
        ''' Add parsed answer to the list of answers. '''
        answers.append(answer)

    return answers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split and print out StackOverflow answers")
    parser.add_argument("answer_file", help="JSON formatted answers from StackOverflow")
    args = parser.parse_args()
    answers = parseAnswers(args.answer_file)
    jsonpickle.set_encoder_options('json', indent=2)
    print jsonpickle.encode(answers, unpicklable=False)
