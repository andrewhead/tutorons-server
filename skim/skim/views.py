#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render


def home(request):
    query = request.GET.get("q", "Java sleep milliseconds")
    context = {"query": query}
    return render(request, "skim/index.html", context)
