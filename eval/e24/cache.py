#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import requests
import requests_cache
import time


logging.basicConfig(level=logging.INFO, format="%(message)s")
CACHE_NAME = 'cache'

requests_cache.install_cache(CACHE_NAME)
session = requests_cache.CachedSession()


def throttle_hook(timeout=1.0):
    ''' 
    Hook for throttling requests if not in cache.
    Snippet from http://requests-cache.readthedocs.org/en/latest/user_guide.html#usage. 
    '''
    def hook(response, *args, **kwargs):
        if not getattr(response, 'from_cache', False):
            print "Pulling anew: caching"
            time.sleep(timeout)
        else:
            print "Found cached file, not sleeping."
        return response
    return hook


def get_session(timeout=1.0):
    session.hooks = {'response': throttle_hook(timeout)}
    return session

