#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import requests
import jsonpickle

import parse


# @cache_page(60 * 60)
def home(request):
    query = request.GET.get('q', "Java sleep milliseconds")
    questionUrl = 'https://api.stackexchange.com/2.2/search/advanced'

    questions = requests.get(questionUrl, params={
        'order': 'desc',
        'sort': 'votes',
        'q': query,
        'site': 'stackoverflow',
        'filter': '!9YdnSK0R1',
        }).json()

    parsedQuestions = parse.parseQuestions(questions)

    questionIds = ';'.join(str(q.id_) for q in parsedQuestions);
    answerUrl = 'https://api.stackexchange.com/2.2/questions/' + str(questionIds) + '/answers'
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
        'questions': jsonpickle.encode(parsedQuestions, unpicklable=False), 
    }
    return render(request, 'skim/index.html', context)
        

