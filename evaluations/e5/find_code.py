#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import json
from bs4 import BeautifulSoup
import codecs


logging.basicConfig(level=logging.INFO, format="%(message)s")


ANSWER_JSON = 'answers.json'
QUESTION_JSON = 'questions.json'
ANSWER_CSV = 'answer_code.csv'
QUESTION_CSV = 'question_code.csv'


def get_first_and_last_lines(example):
    line_sets = []
    soup = BeautifulSoup(example['body'])
    if soup.pre:
        for pre in soup.find_all('pre'):
            lines = pre.text.split('\n')
            first_line = lines[0]
            last_line = lines[-2] if len(lines) > 1 else lines[-1]
            line_sets.append([first_line, last_line])
    return line_sets


def answers_to_csv(answers):
    with codecs.open(ANSWER_CSV, mode='w', encoding='utf8') as acsv:
        acsv.write("QID@AID@First Line@Last Line\n")
        for a in answers['items']:
            line_sets = get_first_and_last_lines(a)
            for line_set in line_sets:
                acsv.write("%d@%d@%s@%s\n" % (a['question_id'], a['answer_id'], line_set[0], line_set[1]))


def questions_to_csv(questions):
    with codecs.open(QUESTION_CSV, mode='w', encoding='utf8') as qcsv:
        qcsv.write("QID@First Line@Last Line\n")
        for q in questions['items']:
            line_sets = get_first_and_last_lines(q)
            for line_set in line_sets:
                qcsv.write("%d@%s@%s\n" % (q['question_id'], line_set[0], line_set[1]))


def main():
    with open(QUESTION_JSON) as qjson:
        questions = json.load(qjson)
    with open(ANSWER_JSON) as ajson:
        answers = json.load(ajson)
    questions_to_csv(questions)
    answers_to_csv(answers)


if __name__ == '__main__':
    main()
