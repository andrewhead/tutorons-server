#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
from django.shortcuts import render


logging.basicConfig(level=logging.INFO, format="%(message)s")


def home(request):
    return render(request, 'home.html', {})
