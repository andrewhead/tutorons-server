#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from tutorons.common.models import ServerQuery, ClientQuery, Region, View
from tastypie import fields


class WriteOnlyMeta(object):
    '''
    With this 'meta', any user is allowed to write any type of list.
    They are prohibited from doing anything else, including inspecting existing data.
    '''
    authorization = Authorization()
    detail_allowed_methods = []
    list_allowed_methods = ['post']


'''
ServerQueryResource and RegionResource are just specified so they can be used as foreign keys for
ClientQueryResource and ViewResource.  There should not be a visible API to these resources.
'''


class ServerQueryResource(ModelResource):

    class Meta:
        queryset = ServerQuery.objects.all()
        resource_name = 'server_query'
        filtering = {
            'path': ALL,
        }


class RegionResource(ModelResource):

    class Meta:
        queryset = Region.objects.all()
        resource_name = 'region'
        filtering = {
            'query': ALL_WITH_RELATIONS,
        }


''' The following resources are actually intended to be visible to API callers. '''


class ClientQueryResource(ModelResource):
    server_query = fields.ForeignKey(ServerQueryResource, 'server_query')

    class Meta(WriteOnlyMeta):
        queryset = ClientQuery.objects.all()
        resource_name = 'client_query'
        filtering = {
            'path': ALL_WITH_RELATIONS,
        }


class ViewResource(ModelResource):
    server_query = fields.ForeignKey(ServerQueryResource, 'server_query')
    region = fields.ForeignKey(RegionResource, 'region')

    class Meta(WriteOnlyMeta):
        queryset = View.objects.all()
        resource_name = 'view'
        filtering = {
            'query': ALL_WITH_RELATIONS,
        }
