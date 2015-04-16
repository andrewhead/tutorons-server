#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import requests
import requests_cache
import json
import time
import codecs
import argparse


logging.basicConfig(level=logging.WARNING, format="%(message)s")
URL = "http://searchcode.com/api/codesearch_I/"
RESULTS_FILE = "results/github.txt"
LINES_FILE = "lines/github.txt"


''' Snippet from http://requests-cache.readthedocs.org/en/latest/user_guide.html#usage. '''
def throttle_hook(timeout=1.0):
    def hook(response, *args, **kwargs):
        if not getattr(response, 'from_cache', False):
            print "Sleep"
            time.sleep(timeout)
        else:
            print "Found cached file, not sleeping."
        return response
    return hook


def fetch_results(session):

    # Fetch lines of code that contain wget
    page = 0
    results = []
    while page is not None and page < 49:
        resp = session.get(URL, params={
            'q': 'wget',
            'p': page,
            'src': 2,                  # Sources indexed Github
            'lan': [41, 31, 69, 78],   # Bourne Again shell, Bourne shell, C shell, Korn shell
            'per_page': 100,
        })
        respJson = resp.json()
        results.extend(respJson['results'])
        page = respJson['nextpage']

    return results


def results_to_file(results):

    # Print all lines that start with 'wget'
    with codecs.open(RESULTS_FILE, 'w', encoding='utf8') as rfile:
        for r in results:
            rfile.write("===File {fn}, {id}===\n".format(fn=r['filename'], id=r['id']))
            rfile.write("\n".join(r['lines'].values()) + "\n")


def lines_to_file(results):

    with codecs.open(LINES_FILE, 'w', encoding='utf8') as lfile:
        for r in results:
            for l in r['lines'].values():
                if l.strip().startswith('wget'):
                    lfile.write(l.strip() + "\n")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="process wget examples from searchcode")
    parser.add_argument('-r', action='store_const', const=True, help="Output results to results.txt")
    args = parser.parse_args()

    # Setup cache for search.
    requests_cache.install_cache('cache')
    session = requests_cache.CachedSession()
    session.hooks = {'response': throttle_hook(0.5)}

    results = fetch_results(session)
    if args.r:
        results_to_file(results)
    lines_to_file(results)

