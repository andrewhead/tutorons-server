#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import subprocess
import requests
import json


logging.basicConfig(level=logging.INFO, format="%(message)s")


SCRAPE_DIR = "scrape"
QUESTIONS_OUTFILE = 'questions.json'
ANSWERS_OUTFILE = 'answers.json'
ANSWERS = [
    {'question': 3190798, 'answer': 3219849},
    {'question': 14104228, 'answer': 14104369},
    {'question': 364015, 'answer': 364074},
    {'question': 12872387, 'answer': 12872443},
    {'question': 8115087, 'answer': 8115155},
    {'question': 25221352, 'answer': 25222518},
    {'question': 12591832, 'answer': 12591905},
    {'question': 27391812, 'answer': 27414401},
    {'question': 4683639, 'answer': 4684210},
    {'question': 5362732, 'answer': 5362764},
    {'question': 27045539, 'answer': 27523599},
    {'question': 19618268, 'answer': 19618531},
    {'question': 19087332, 'answer': 19087631},
    {'question': 26759118, 'answer': 26759193},
    {'question': 5931223, 'answer': 5931253},
    {'question': 4362491, 'answer': 4362514},
    {'question': 2187821, 'answer': 2187834},
    {'question': 9505971, 'answer': 9506077},
    {'question': 23740288, 'answer': 23740522},
    {'question': 9003288, 'answer': 9003638},
]
QUESTIONS = [
    4980414,
    18851438,
    22705019,
    2592798,
    21219150,
    14917510,
    2130446,
    6233805,
    27436551,
    17828552,
    3929301,
    27889586,
    9893851,
    23877406,
    1283646,
    23438583,
    12332532,
    17383236,
    25356695,
    15234524,
]


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
            'pagesize': '100',
            'filter': '!9YdnSJ*_S',
            }).json()
        more_questions = questions['has_more']
        page_number += 1
        all_questions['items'].extend(questions['items'])
    return all_questions


def fetch_answers(answer_ids):
    answer_param = ';'.join([str(a) for a in answer_ids])
    answer_url = 'https://api.stackexchange.com/2.2/answers/' + answer_param
    more_answers = True
    page_number = 1
    all_answers = {'items': []}
    while more_answers:
        answers = requests.get(answer_url, params={
            'site': 'stackoverflow',
            'page': page_number,
            'pagesize': '100',
            'filter': '!9YdnSM68i',
            }).json()
        more_answers = answers['has_more']
        page_number += 1
        all_answers['items'].extend(answers['items'])
    return all_answers


def wget_address(address):
    subprocess.call([
        "wget",
        "-P", SCRAPE_DIR,       # output to a scrape directory
        "--adjust-extension",   # download HTML pages with .html extension
        "-nc",                  # don't download the same file twice
        "-w", "1",              # wait 1s between requests
        "-p", "-k",             # for downloading stylesheets (doesn't work?)
        address,
    ])


def main():
    ''' Get ground truth answers from StackExchange API. '''
    questions = fetch_questions(QUESTIONS)
    answers = fetch_answers([a['answer'] for a in ANSWERS])
    with open(QUESTIONS_OUTFILE, 'w') as qof:
        json.dump(questions, qof, indent=2)
    with open(ANSWERS_OUTFILE, 'w') as aof:
        json.dump(answers, aof, indent=2)

    ''' StackOverflow content gets fetched to folder "stackoverflow.com" '''
    for q in QUESTIONS:
        wget_address("http://www.stackoverflow.com/questions/%d" % q)
    for a in ANSWERS:
        wget_address("www.stackoverflow.com/a/%d/%d" % (a['question'], a['answer']))


if __name__ == '__main__':
    main()
