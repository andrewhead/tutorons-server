#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
import requests
import json
from collections import defaultdict
from bs4 import BeautifulSoup
from markdown import markdown
import codecs


QUESTION_FILE = "questions.json"
ANSWER_FILE = "answers.json"
PRINTOUT_FILE = "printout.txt"


def fetch_questions(question_ids):
    question_param = ';'.join([str(q) for q in question_ids])
    answer_url = 'https://api.stackexchange.com/2.2/questions/' + question_param
    more_questions = True
    page_number = 1
    all_questions = {'items': []}
    while more_questions:
        questions = requests.get(answer_url, params={
            'site': 'stackoverflow',
            'page': page_number,
            'pagesize': '100',           # No of Answers
            'filter': '!9YdnSJ*_S',
            }).json()
        more_questions = questions['has_more']
        page_number += 1
        all_questions['items'].extend(questions['items'])
    return all_questions


def fetch_answers(question_ids):
    question_param = ';'.join([str(q) for q in question_ids])
    answer_url = 'https://api.stackexchange.com/2.2/questions/' + question_param + '/answers'
    more_answers = True
    page_number = 1
    all_answers = {'items': []}
    while more_answers:
        answers = requests.get(answer_url, params={
            'site': 'stackoverflow',
            'page': page_number,
            'pagesize': '100',           # No of Answers
            'filter': '!-*f(6sno9fyP',
            }).json()
        more_answers = answers['has_more']
        page_number += 1
        all_answers['items'].extend(answers['items'])
    return all_answers


def main():
    question_ids = [
        36932,
        89228,
        312443,
        166506,
        38987,
        613183,
        546321,
        287871,
        60208,
        1305532,
        89178,
        1916218,
        18686860,
    ]

    ''' Get questions and answers, sort answers by question_id. '''
    questions = fetch_questions(question_ids)
    answers = fetch_answers(question_ids)
    sorted_answers = defaultdict(list)
    for a in answers['items']:
        sorted_answers[int(a['question_id'])].append(a)

    ''' Write questions and answers to files. '''
    with open(QUESTION_FILE, 'w') as q_file:
        json.dump(questions, q_file, indent=2)
    with open(ANSWER_FILE, 'w') as a_file:
        json.dump(sorted_answers, a_file, indent=2)

    body_text = lambda body: BeautifulSoup(body).text

    with codecs.open(PRINTOUT_FILE, mode='w', encoding='utf8') as p_file:
        for q in questions['items']:
            qid = q['question_id']
            print("Question " + str(qid), file=p_file)
            print("", file=p_file)
            print(body_text(q['body']), file=p_file)
            print("", file=p_file)
            for a in sorted_answers[int(qid)]:
                print("----------------\n", file=p_file)
                print("Answer " + str(a['answer_id']), file=p_file)
                print("To question " + str(qid), file=p_file)
                print("", file=p_file)
                print(body_text(a['body']), file=p_file)
                print("", file=p_file)
            print("================\n", file=p_file)


if __name__ == '__main__':
    main()
