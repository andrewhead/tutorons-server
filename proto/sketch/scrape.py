#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")

D3_EXAMPLES_URL = 'http://christopheviau.com/d3list/index.html' 

def main():
    resp = requests.get(D3_EXAMPLES_URL)
    soup = BeautifulSoup(resp)
    soup.ol.find_all('li')


if __name__ == '__main__':
    main()

