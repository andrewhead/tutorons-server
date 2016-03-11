#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from django.http import HttpResponse
import json

from tutorons.common.htmltools import get_css_selector, HtmlDocument
from tutorons.common.dblogger import DBLogger


logging.basicConfig(level=logging.INFO, format="%(message)s")


def _package_region(region, document, region_id, query_id):
    return {
        'node': get_css_selector(region.node),
        'start_index': region.start_offset,
        'end_index': region.end_offset,
        'document': document,
        'region_id': region_id,
        'query_id': query_id,
    }


def pagescan(scan_func):
    '''
    A wrapper around 'scan' views.
    Handles a lot of the "scanning" boilerplate of fetching request
    arguments, logging the request and its results, and retturning the
    results as and HTTP response.
    '''
    def wrapper(request):

        document_content = request.POST.get('document')
        client_req_time = request.POST.get('client_start_time')

        # Log request information
        db_logger = DBLogger()
        query_record = db_logger.log_query(request)

        # Scan document with wrapped method to get regions
        # and their explanations
        document = HtmlDocument(document_content)
        regions = scan_func(document)
        regions_explained = []
        for region, explanation in regions:
            region_record = db_logger.log_region(request, query_record, region)
            regions_explained.append(
                _package_region(region, explanation, region_record.id, query_record.id)
            )

        # Update the runtime of the scan
        db_logger.update_server_end_time(query_record)

        # Send back a response
        return HttpResponse(
            json.dumps({
                'regions': regions_explained,
                'url': "http://localhost:8002/api/v1/client_query/",
                'query_id': query_record.id,
                'client_start_time': client_req_time,
            }, indent=2))

    return wrapper
