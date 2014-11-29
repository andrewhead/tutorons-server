#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from enum import Enum
import argparse
import json
import jsonpickle
from bs4 import BeautifulSoup
import re


class Question(object):
    
    def __init__(self, id_, title):
        self.id_ = id_
        self.title = title


class Answer(object):

    def __init__(self, id_, qid_, body, votes, reputation):
        self.id_ = id_
        self.qid_ = qid_ # question id
        self.lines = []
        self.body = body
        self.votes = votes
        self.reputation = reputation
 
    def append(self, line):
        self.lines.append(line)


class Line(object):

    def __init__(self, text, type_, references=None, concepts=None):
        self.text = text
        self.type_ = type_
        self.references = references or []
        self.concepts = concepts or []

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


class Concept(Enum):
    ARITHMETIC_OP = "Arithmetic",
    RELATIONAL_OP = "Relations",
    LOOP = "Loop",
    ASSIGNMENT = "Assign",
    CONDITIONAL = "Conditional",
    RETURN = "Return",
    ARRAY = "Array",
    FUNCTION = "Function",
    OBJECT = "Object",

    def __getstate__(self):
        ''' When converting to JSON, return the associated string. '''
        return self.value[0]


def getClass(string):
    stripped = string.strip()
    if not re.search("^[A-Z]", stripped):
        return None
    else:
        return stripped.split(".")[0]


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
            if getClass(ref.text):
                line.addReference(getClass(ref.text))
        lines.append(line)
    return lines


def parseClasses(codeText):
    classes = []
    declMatch = re.match('^\s*([A-Z]\w+)\s+\w+\s*(;|=\s*)', codeText)
    if declMatch:
        classes.append(declMatch.group(1))
    newMatches = re.findall('new\s+([A-Z][A-Za-z0-9_]*)\s*\(', codeText)
    classes.extend(newMatches)
    return classes


def parseConcepts(codeText):
    concepts = set()
    kw = lambda term: '(^|\s+)' + term + '\W'
    patterns = {
        " [-/+*] |\+\+": Concept.ARITHMETIC_OP,
        "[<>]|==|!=": Concept.RELATIONAL_OP,
        kw("(for|while)"): Concept.LOOP,
        "[^=]=[^=]": Concept.ASSIGNMENT,
        kw("if"): Concept.CONDITIONAL,
        kw("return"): Concept.RETURN,
        "\[": Concept.ARRAY,
        kw("new"): Concept.OBJECT,
        kw("(public|private)") + ".*\(.*[^;]$": Concept.FUNCTION,
    }
    for patt, concept in patterns.items():
        if re.search(patt, codeText):
            concepts.add(concept)
    return list(concepts)


def isJava(line):
    ''' Rule out XML '''
    if re.search("^\s*<", line) or re.search(">\s*$", line):
        return False
    return True


def parseCode(codeTag):
    ''' Process code blocks. '''
    lines = []
    commentState = CommentState.CLOSED

    for line in codeTag.text.rstrip().split('\n'):

        concepts = []

        ''' Check for comment start. '''
        if commentState == CommentState.CLOSED and re.match('.*/\*.*', line):
            commentState = CommentState.OPEN

        ''' Capture references to classes. '''
        references = []
        if commentState == CommentState.CLOSED:
            if isJava(line):
                concepts.extend(parseConcepts(line))
                references.extend(parseClasses(line))

        ''' Capture comments. '''
        if commentState == CommentState.OPEN:
            type_ = LineType.CODE_COMMENT_LONG
            if re.match('.*\*/.*', line):
                commentState = CommentState.CLOSED
        elif commentState == CommentState.CLOSED and re.match('.*//.*', line):
            type_ = LineType.CODE_COMMENT_INLINE
        else:
            type_ = LineType.CODE

        lines.append(Line(line, type_, references, concepts))

    return lines


def parseAnswers(answerData):

    answers = []
    for item in answerData['items']:
        ''' Create answer. '''
        answer = Answer(item['answer_id'], item['question_id'], item['body'], item['score'], item['owner'].get('reputation', 0))

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


def parseQuestions(questionData):
    
    questions = []
    for item in questionData['items']:
        ''' Create Question '''
        question = Question(item['question_id'], item['title'])
        questions.append(question)
    return questions
