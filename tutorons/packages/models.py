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


class QuestionSnapshot(models.Model):
    '''
    A snapshot of a Stack Overflow question at a moment when the API is queried.
    This contains much of the same data as the "Post" model.
    Though 'Snapshot' models come from periodic queries to the Stack Overflow API,
    rather than from a one-time data dump.  This allows us to describe the longitudinal change
    in Stack Overflow posts and data.
    '''

    # Fetch logistics
    fetch_index = models.IntegerField()
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    question_id = models.IntegerField(db_index=True)
    owner_id = models.IntegerField(null=True)
    comment_count = models.IntegerField()
    delete_vote_count = models.IntegerField()
    reopen_vote_count = models.IntegerField()
    close_vote_count = models.IntegerField()
    is_answered = models.BooleanField()
    view_count = models.IntegerField()
    favorite_count = models.IntegerField()
    down_vote_count = models.IntegerField()
    up_vote_count = models.IntegerField()
    answer_count = models.IntegerField()
    score = models.IntegerField()
    last_activity_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    title = models.TextField()
    body = models.TextField()

    class Meta:
        db_table = "questionsnapshot"


class Tag(models.Model):
    ''' A tag for Stack Overflow posts. '''
    # We will look up tags based on their tag names when making PostTags
    tag_name = models.CharField(db_index=True, max_length=70)
    count = models.IntegerField()
    excerpt_post_id = models.IntegerField(db_index=True, null=True)
    wiki_post_id = models.IntegerField(null=True)

    class Meta:
        db_table = "tag"


class QuestionSnapshotTag(models.Model):
    ''' A link between one snapshot of a Stack Overflow question and one of its tags. '''
    # Both IDs are indexed to allow fast lookup of question snapshot for a given tag and vice versa.
    question_snapshot_id = models.IntegerField(db_index=True)
    tag_id = models.IntegerField(db_index=True)

    question_snapshot = models.ForeignKey(QuestionSnapshot, db_column='question_snapshot_id', to_field='id')
    tag = models.ForeignKey(Tag, db_column='tag_id', to_field='id')

    class Meta:
        db_table = "questionsnapshottag"


class GitHubProject(models.Model):
    ''' A project on GitHub. '''

    # Fetch logistics
    fetch_index = models.IntegerField()
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    # These identifiers identify the project from different contexts.
    # 'name' will give the name of a package that has a GitHub project.
    # 'owner' and 'repo' uniquely identify a GitHub project and provide
    # the URL through which we reach it in the API.
    name = models.TextField(db_index=True)
    owner = models.TextField()
    repo = models.TextField()

    class Meta:
        db_table = "githubproject"


class Issue(models.Model):
    '''
    An issue for a GitHub project.
    The 'body' field is nullable as we found during our initial fetch that some
    of the issues data contained 'null' bodies.
    '''

    # Fetch logistics
    fetch_index = models.IntegerField()
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    github_id = models.IntegerField()
    project = models.ForeignKey(GitHubProject)

    # Fields from the GitHub API
    number = models.IntegerField()
    created_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(db_index=True)
    closed_at = models.DateTimeField(db_index=True, null=True)
    state = models.TextField()
    body = models.TextField(null=True)
    comments = models.IntegerField()

    class Meta:
        db_table = "issue"


class IssueEvent(models.Model):
    ''' An event (e.g., "closed") for an issue for a GitHub project. '''

    fetch_index = models.IntegerField()
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    github_id = models.IntegerField()
    issue = models.ForeignKey(Issue)
    created_at = models.DateTimeField(db_index=True)
    event = models.TextField()

    class Meta:
        db_table = "issueevent"


class IssueComment(models.Model):
    ''' A comment on a GitHub issue. '''

    fetch_index = models.IntegerField()
    date = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    github_id = models.IntegerField()
    issue = models.ForeignKey(Issue)
    created_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(db_index=True)
    body = models.TextField()

    class Meta:
        db_table = "issuecomment"
