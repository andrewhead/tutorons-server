#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import requests
import copy
import json


logging.basicConfig(level=logging.INFO, format="%(message)s")
URL = 'http://127.0.0.1:8000/test'


def main():
    
    spec1 = {
        'subject': 'the light',
        'verb': 'be',
        'object': 'on',
        'tense': 'PAST',
    }
    spec2 = copy.copy(spec1)
    spec2['tense'] = 'PRESENT'
    spec3 = copy.copy(spec1)
    spec3['tense'] = 'FUTURE'
    specs = [spec1, spec2, spec3]

    for spec in specs:
        resp = requests.get(URL, params={'spec': json.dumps(spec)})
        logging.info(resp.text)


if __name__ == '__main__':
    main()

