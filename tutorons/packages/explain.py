#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from tutorons.packages.models import WebPageVersion, WebPageContent, Search, SearchResult, SearchResultContent, Code
import cache
import logging
import slumber
import time

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(message)s")
default_requests_session = cache.get_session(timeout=1)
default_requests_session.headers['User-Agent'] =\
    "Andrew Head (for academic analysis) <andrewhead@eecs.berekeley.edu, Austin Le (for academic" +\
    " analysis) <austinhle@berkeley.edu>"

def make_request(method, *args, **kwargs):
    MAX_ATTEMPTS = 5
    RETRY_DELAY = 30
    try_again = True
    attempts = 0
    res = None

    def log_error(err_msg):
        logging.warn(
            "Error (%s) For API call %s, Args: %s, Kwargs: %s",
            str(err_msg), str(method), str(args), str(kwargs)
        )

    while try_again and attempts < MAX_ATTEMPTS:
        try:
            res = method(*args, **kwargs)
            if hasattr(res, 'status_code') and res.status_code not in [200]:
                log_error(str(res.status_code))
                res = None
            try_again = False
        except (slumber.exceptions.HttpNotFoundError):
            log_error("Not Found")
            try_again = False
        except slumber.exceptions.HttpServerError:
            log_error("Server 500")
            try_again = False
        except requests.exceptions.ConnectionError:
            log_error("ConnectionError")
        except requests.exceptions.ReadTimeout:
            log_error("ReadTimeout")

        if try_again:
            logging.warn("Waiting %d seconds for before retrying.", int(RETRY_DELAY))
            time.sleep(RETRY_DELAY)
            attempts += 1

    return res


def explain(package):
    NPM_url = "https://www.npmjs.com/package/{pkg}".format(pkg=package)
    res = make_request(default_requests_session.get, NPM_url)
    if res is not None:
        page = BeautifulSoup(res.content, 'html.parser')
        readme = str(page.select('div#readme')[0])
        description = page.select('p.package-description')[0].text
        url = NPM_url

    documented_since = get_documented_since(package)

    response_time, resolution_time = get_response_time(package), get_resolution_time(package)

    num_questions = get_num_questions(package)

    results_with_code = get_results_with_code(package)

    return description, documented_since, url, response_time, resolution_time, num_questions, results_with_code


def get_documented_since(p):
    documented_since = (SearchResult.objects
        .filter(search_id=models.F('search__id'))
        .filter(web_page_version__url=models.F('url'))
        .filter(search__fetch_index=13)
        .filter(search__package=p)
        .aggregate(models.Min('web_page_version__timestamp'))['web_page_version__timestamp__min']
    )
    return documented_since


def get_response_time(p):
    # TODO: Fetch response_time from GitHub issues.
    return '1 day'


def get_resolution_time(p):
    # TODO: Fetch resolution_time from GitHub issues.
    return '3.5 days'


def get_num_questions(p):
    # TODO: Fetch num_questions by doing a join between the `tag` table, the `questionsnapshottag` table, and the `questionsnapshot` tables
    return 50


def get_results_with_code(p):
    # TODO: Fetch results_with_code using a Django version of Andrew's JavaScript code on Package-Community.
    # See example.sql for the translated SQL query.
    return 100
