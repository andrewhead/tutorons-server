#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from tutorons.common.htmltools import get_css_selector
from tutorons.common.dblogger import DBLogger
from tutorons.common.htmltools import HtmlDocument
from django.http import HttpResponse
import json

logging.basicConfig(level=logging.INFO, format="%(message)s")
region_logger = logging.getLogger('region')


def package_region(region, document, rid, qid):
    return {
        'node': get_css_selector(region.node),
        'start_index': region.start_offset,
        'end_index': region.end_offset,
        'document': document,
        'region_id' : rid,
        'query_id' : qid,
    }


def log_region(r, url):
    region_logger.info(',,,'.join([
        'Origin:%s',
        'Path:%s',
        'Text:%s',
        'Range:[%d,%d]'
    ]), url, get_css_selector(r.node), r.string, r.start_offset, r.end_offset)


def get_descendants(x):
    ''' Get all descendants of an object. '''

    if isinstance(x, list):
        return [i for el in x for i in get_descendants(el)]
    elif hasattr(x, '__dict__'):
        return [x] + [i for child in x.__dict__.values() for i in get_descendants(child)]
    elif isinstance(x, dict):
        return [i for child in x for i in get_descendants(child)]
    else:
        return []

def dec(scan):
    def proc_request(request):
        db_logger = DBLogger()
        doc_body = request.POST.get('document')
        origin = request.POST.get('origin')
        client_start_time = request.POST.get('client_start_time')
        region_logger.info("Request for page from origin: %s", origin)
        qid = db_logger.log_query(request)
        document = HtmlDocument(doc_body)
        regions = scan(document)
        explained_regions = []
        for r, d in regions:
            log_region(r, origin)
            rid = db_logger.log_region(request, r)
            explained_regions.append(package_region(r, d, rid, qid))
        db_logger.update_server_end_time(qid)
        return HttpResponse(json.dumps({"explained_regions": explained_regions,
                                        "url": "http://localhost:8002/api/v1/client_query/",
                                        "sq_id": qid,
                                        "client_start_time": client_start_time}, indent=2))
    return proc_request