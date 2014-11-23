#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render
import parse
import requests
import jsonpickle


def home(request):
    query = request.GET.get('q', "Java sleep milliseconds")
    questionUrl = 'https://api.stackexchange.com/2.2/search/advanced'
    question = requests.get(questionUrl, params={
        'order': 'desc',
        'sort': 'votes',
        'q': query,
        'site': 'stackoverflow',
        'filter': '!9YdnSK0R1',
    }).json()['items'][0]
    questionId = int(question['question_id'])

    answerUrl = 'https://api.stackexchange.com/2.2/questions/' + str(questionId) + '/answers'
    answers = requests.get(answerUrl, params={
        'order': 'desc',
        'sort': 'activity',
        'site': 'stackoverflow',
        'filter': '!b0OfNZ*ohL7Iue',
    }).json()
    parsedAnswers = parse.parseAnswers(answers)

    context = {
        'query': query,
        'answers': jsonpickle.encode(parsedAnswers, unpicklable=False),
    }
    return render(request, 'skim/index.html', context)
