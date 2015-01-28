#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import requests
import json


API_URL = "https://www.googleapis.com/customsearch/v1"
API_KEY = "AIzaSyBcHH5JqkalO6atnpCqZCjvFWFiT8-yC8k"
SEARCH_ID = "011356320933563804135:byoi9uglfjg"

OUT_FILE = "results.json"


def main():
    resp = requests.get(API_URL, params={
        'q': 'java write to file', 
        'key': API_KEY,
        'cx': SEARCH_ID
    })
    with open(OUT_FILE, 'w') as results_file:
        json.dump(resp.json(), results_file, indent=2)


if __name__ == '__main__':
    main()
