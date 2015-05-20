#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import requests
import json
import time
import cache
import codecs


API_URL = 'https://www.googleapis.com/customsearch/v1'
API_KEY = 'AIzaSyBcHH5JqkalO6atnpCqZCjvFWFiT8-yC8k'
SEARCH_ID = '011356320933563804135:byoi9uglfjg'

RESULTS_FILE = 'results.json'
LINKS_FILE = 'links.csv'


def fetch_results(session, query, page_size=10, num_results=100, delay=1):

    results = []
    start = 1

    while len(results) < num_results:
        resp = session.get(API_URL, params={
            'q': query, 
            'key': API_KEY,
            'cx': SEARCH_ID,
            'num': page_size,
            'start': start
        })
        respJson = resp.json()
        results.extend(respJson['items'])
        start += page_size

    return results


def write_links_file(results, delimiter='@'):
    ''' 
    I failed to see '@' in any titles or links, so it should work as a default 
    delimiter at least in the current case.        
    '''

    with codecs.open(LINKS_FILE, 'w', 'utf8') as links_file:
        index = 1
        for r in results:
            links_file.write(
                delimiter.join(
                    [unicode(_) for _ in [index, r['link'], r['title']]]
                ) + '\n')
            index += 1


def write_results_file(results):

    with open(RESULTS_FILE, 'w') as results_file:
        json.dump(results, results_file, indent=2)


if __name__ == '__main__':
    session = cache.get_session()
    results = fetch_results(session, "how to scrape a website")
    write_results_file(results)
    write_links_file(results)
