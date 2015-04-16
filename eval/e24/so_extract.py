#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import math
import cache
import codecs
import re
from bs4 import BeautifulSoup as Soup


logging.basicConfig(level=logging.INFO, format="%(message)s")
API_URL = "https://api.stackexchange.com"
QUESTION_URL = API_URL + "/2.2/search/advanced"
ANSWER_URL = API_URL + "/2.2/questions/{qids}/answers"

QUESTION_RESULTS = "results/so_questions.txt"
ANSWER_RESULTS = "results/so_answers.txt"
QUESTION_LINES = "lines/so_questions.txt"
ANSWER_LINES = "lines/so_answers.txt"


def fetch_questions(session, query):
    ''' Fetch 1000 questions related to query '''
    page = 1
    all_questions = []
    while page is not None and page <= 10:
        questions = session.get(QUESTION_URL, params={
            'site': 'stackoverflow',
            'q': query,
            'sort': 'relevance',
            'order': 'desc',
            'pagesize': '100',
            'page': page,
            'filter': '!9YdnSJ*_S',
            }).json()
        page = page + 1 if questions['has_more'] else None
        all_questions.extend(questions['items'])
    return all_questions


def fetch_answers(session, questions):
    ''' Get all answers to StackOverflow questions. '''

    all_answers = []
    qid_list = [q['question_id'] for q in questions]
    BATCH = 10

    for batch in range(0, int(math.ceil(float(len(qid_list)) / BATCH))):
        qids = qid_list[batch * BATCH : (batch + 1) * BATCH]
        qid_str = ';'.join(str(qid) for qid in qids)
        answer_url = ANSWER_URL.format(qids=qid_str)

        page = 1
        while page is not None:
            answers = session.get(answer_url, params={
                'site': 'stackoverflow',
                'sort': 'votes',
                'order': 'desc',
                'pagesize': '100',
                'page': page,
                'filter': '!9YdnSM68i',
                }).json()
            page = page + 1 if answers['has_more'] else None
            all_answers.extend(answers['items'])

    return all_answers


def answer_results_to_file(results):

    with codecs.open(ANSWER_RESULTS, 'w', encoding='utf8') as rfile:
        for r in results:
            rfile.write("===Answer {id}===\n".format(id=r['answer_id']))
            soup = Soup(r['body'])
            for tag in soup.children:
                if tag.name == 'pre':
                    rfile.write(tag.text + "\n")
                    rfile.write("--------------\n")


def answer_lines_to_file(results):

    with codecs.open(ANSWER_LINES, 'w', encoding='utf8') as lfile:
        for r in results:
            soup = Soup(r['body'])
            for tag in soup.children:
                if tag.name == 'pre':
                    text = re.sub(r'\\s*\n', '', tag.text)  # remove line continuations
                    lines = text.split('\n')
                    for line in lines:
                        if line.strip().startswith('wget'):
                            lfile.write(line.strip() + '\n')


def question_results_to_file(results):

    with codecs.open(QUESTION_RESULTS, 'w', encoding='utf8') as rfile:
        for r in results:
            rfile.write("===QUESTION {id}===\n".format(id=r['question_id']))
            soup = Soup(r['body'])
            for tag in soup.children:
                if tag.name == 'pre':
                    rfile.write(tag.text + "\n")
                    rfile.write("--------------\n")


def question_lines_to_file(results):

    with codecs.open(QUESTION_LINES, 'w', encoding='utf8') as lfile:
        for r in results:
            soup = Soup(r['body'])
            for tag in soup.children:
                if tag.name == 'pre':
                    text = re.sub(r'\\s*\n', '', tag.text)  # remove line continuations
                    lines = text.split('\n')
                    for line in lines:
                        if re.match("^(.*\$)?\s*wget", line):
                            line = re.sub("^.*\$\s*", "", line)
                            lfile.write(line.strip() + '\n')


if __name__ == '__main__':
    session = cache.get_session(timeout=1.0)
    questions = fetch_questions(session, 'wget')
    answers = fetch_answers(session, questions)
    answer_results_to_file(answers)
    answer_lines_to_file(answers)
    question_results_to_file(questions)
    question_lines_to_file(questions)

