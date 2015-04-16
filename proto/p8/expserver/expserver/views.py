from __future__ import unicode_literals
import logging
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as Soup


def regex(request, regex):
    resp = requests.get(
       "http://rick.measham.id.au/paste/explain.pl",
       params={'regex': regex}
    )
    exp = Soup(resp.text).find_all('pre')[0]
    return HttpResponse(exp.text)
