#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import json
from bs4 import BeautifulSoup
import ast


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


PREVIEW_LEN = 20
ANSWER_JSON = 'answers.json'
QUESTION_JSON = 'questions.json'


def parse_code(code_text, ids):
    id_str = ",".join(["%s" % (str(val)) for (key, val) in ids.items()])
    preview = code_text.split('\n')[0][:PREVIEW_LEN]
    try:
        tree = ast.parse(code_text)
    except Exception as e:
        logging.error("%s,%s,%s,%d,%d,%s", id_str, preview, type(e).__name__, e.lineno, e.offset, e.text.strip())
        tree = None
    else:
        logging.info("%s,%s,success", id_str, preview)
    return tree


def parse_code_in_example(example, id_fields):
    soup = BeautifulSoup(example['body'])
    if soup.pre:
        ids = {f: example[f] for f in id_fields}
        for pre in soup.find_all('pre'):
            parse_code(pre.text, ids) 


def main():
    with open(QUESTION_JSON) as qjson:
        questions = json.load(qjson)['items']
    with open(ANSWER_JSON) as ajson:
        answers = json.load(ajson)['items']

    logging.info("Parsing Questions")
    for q in questions:
        parse_code_in_example(q, ['question_id'])

    logging.info("Parsing Answers")
    for a in answers:
        parse_code_in_example(a, ['question_id', 'answer_id'])


if __name__ == '__main__':
    main()
