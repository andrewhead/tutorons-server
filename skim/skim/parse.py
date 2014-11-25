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

    def __init__(self, id_, body):
        self.id_ = id_
        self.lines = []
        self.body = body
 
    def append(self, line):
        self.lines.append(line)


class Line(object):

    def __init__(self, text, type_, references=None):
        self.text = text
        self.type_ = type_
        self.references = references or []

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


def parseText(textTag):
    lines = []
    ''' Process text blocks. '''
    for sentence in re.split('\.[\s]', textTag.decode_contents()):
        if sentence == "":
            continue
        sentenceSoup = BeautifulSoup(sentence, 'html.parser')
        line = Line(sentenceSoup.text, LineType.TEXT)
        ''' Look for inline references to variable and class names. '''
        references = sentenceSoup.findAll('code')
        for ref in references:
            line.addReference(ref.text)
        lines.append(line)
    return lines


def parseCode(codeTag):
    ''' Process code blocks. '''
    lines = []
    commentState = CommentState.CLOSED

    for line in codeTag.text.rstrip().split('\n'):

        ''' Check for comment start. '''
        if commentState == CommentState.CLOSED and re.match('.*/\*.*', line):
            commentState = CommentState.OPEN

        ''' Capture references to classes. '''
        references = []
        if commentState == CommentState.CLOSED:
            declMatch = re.match('^\s*([A-Z]\w+)\s+\w+\s*(;|=\s*)', line)
            if declMatch:
                references.append(declMatch.group(1))

        ''' Capture comments. '''
        if commentState == CommentState.OPEN:
            type_ = LineType.CODE_COMMENT_LONG
            if re.match('.*\*/.*', line):
                commentState = CommentState.CLOSED
        elif commentState == CommentState.CLOSED and re.match('.*//.*', line):
            type_ = LineType.CODE_COMMENT_INLINE
        else:
            type_ = LineType.CODE

        lines.append(Line(line, type_, references))

    return lines


def parseAnswers(answerData):

    answers = []
    for item in answerData['items']:

        ''' Create answer. '''
        answer = Answer(item['answer_id'], item['body'])

        ''' Parse the answer to separate lines. '''
        soup = BeautifulSoup(item['body'], 'html.parser')
        tags = [tag for tag in soup.children if tag != '\n']
        for tag in tags:
            if tag.name == 'p':
                answer.lines.extend(parseText(tag))
            elif tag.name == 'pre':
                answer.lines.extend(parseCode(tag))
                    
        ''' Add parsed answer to the list of answers. '''
        answers.append(answer)

    return answers
