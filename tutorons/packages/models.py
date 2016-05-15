#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

import datetime


class WebPageContent(models.Model):
    ''' The contents at a web URL at a point in time. '''

    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    url = models.TextField(db_index=True)
    content = models.TextField()

    class Meta:
        db_table = "webpagecontent"


class WebPageVersion(models.Model):
    # Fetch logistics
    fetch_index = models.IntegerField()
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    url = models.TextField(db_index=True)
    url_key = models.TextField()
    timestamp = models.DateTimeField(db_index=True)
    original = models.TextField()
    mime_type = models.TextField()
    # Status code is a text field as several test records we inspected had "-" for the status
    # instead of some integer value
    status_code = models.TextField(db_index=True)
    digest = models.TextField(db_index=True)
    length = models.IntegerField(null=True)

    class Meta:
        db_table = "webpageversion"


class Search(models.Model):
    ''' A search query made to a search engine. '''

    fetch_index = models.IntegerField()
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    query = models.CharField()
    page_index = models.IntegerField()
    requested_count = models.IntegerField()
    result_count_on_page = models.IntegerField()
    estimated_results_count = models.IntegerField()

    # An optional field for associating a search with a specific package.
    # This should be specified whenever we need to trace a search to a related package.
    package = models.TextField(db_index=True, null=True)

    class Meta:
        db_table = "search"


class SearchResult(models.Model):
    ''' A result to a search query submitted to a search engine. '''

    search = models.ForeignKey(Search, related_name='results', on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    snippet = models.TextField(null=True)
    link = models.CharField()
    url = models.CharField(db_index=True)
    updated_date = models.DateTimeField()
    rank = models.IntegerField()

    # A field used to link a SearchResult with a WebPageVersion, effectively for joining them on the column "url"
    web_page_version = models.ForeignKey(WebPageVersion, db_column='url', to_field='url')

    class Meta:
        db_table = "searchresult"


class SearchResultContent(models.Model):
    ''' A link from search results to the content at the result's URL. '''

    search_result = models.ForeignKey(SearchResult, on_delete=models.SET_NULL, null=True)
    content = models.ForeignKey(WebPageContent, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "searchresultcontent"


class Code(models.Model):
    ''' A snippet of code found on a web page. '''

    # These fields signify when the snippet was extracted
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    compute_index = models.IntegerField(db_index=True)

    web_page = models.ForeignKey(WebPageContent, on_delete=models.SET_NULL, null=True)
    code = models.TextField()

    class Meta:
        db_table = "code"
