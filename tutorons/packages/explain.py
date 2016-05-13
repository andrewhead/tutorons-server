#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tutorons.packages.models import NPMPackageTutoron
import cache
import logging
import slumber
import time

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
    try:
        p = NPMPackageTutoron.objects.get(package=package)
    except ObjectDoesNotExist:
        p = fetch_package_data(package)
        logging.warn("Tried to retrieve object from database that does not exist.")
    except MultipleObjectsReturned:
        logging.warn("Multiple objects in database with the same package name.")

    return p.description, p.documented_since, p.url, p.response_time, p.resolution_time, p.num_questions, p.results_with_code


def fetch_package_data(p):
    NPM_url = "https://www.npmjs.com/package/{pkg}".format(pkg=p.name)
    res = make_request(default_requests_session.get, NPM_url)
    if res is not None:
        page = BeautifulSoup(res.content, 'html.parser')
        p.readme = str(page.select('div#readme')[0])
        p.description = page.select('p.package-description')[0].text
        p.url = NPM_url

    # TODO(austinhle): Fetch documented_since from WebPageVersion model.
    # TODO(austinhle): Fetch response_time, resolution_time from GitHub issues.
    # TODO(austinhle): Fetch num_questions from StackOverflow.
    # TODO(austinhle): Fetch results_with_code from Andrew's scraped data.

    p.save()
    return p
