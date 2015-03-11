#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import requests
import json


API_URL = "https://www.googleapis.com/customsearch/v1"
API_KEY = "AIzaSyBcHH5JqkalO6atnpCqZCjvFWFiT8-yC8k"
SEARCH_ID = "011356320933563804135:byoi9uglfjg"

OUT_FILE = "query_results.json"
QUERIES = [
    'python.h no such file or directory',
    'imshow doesn\'t open',
    'cv2 python read from file',
    'opencv face recognition python',
    'time clock python',
    'get last element d3',
    'svg get text width',
    'fit container set to text size svg',
    'invalid http_host header',
    'multiple domains nginx',
    'supervisorctl add',
    'supervisorctl gunicorn django',
]


def main():

    with open(OUT_FILE, 'w') as results_file:
        for q in QUERIES:
            resp = requests.get(API_URL, params={
                'q': q, 
                'key': API_KEY,
                'cx': SEARCH_ID
            })
            json.dump(resp.json(), results_file, indent=2)


if __name__ == '__main__':
    main()
