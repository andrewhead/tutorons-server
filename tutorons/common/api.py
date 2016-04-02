from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from tutorons.common.models import Block, ServerQuery, ClientQuery, Region, View
from tastypie import fields


class BlockResource(ModelResource):
    class Meta:
        queryset = Block.objects.all()
        resource_name = 'block'
        authorization = Authorization()


class ServerQueryResource(ModelResource):
    class Meta:
        queryset = ServerQuery.objects.all()
        resource_name = 'server_query'
        authorization = Authorization()
        filtering = {
            'path': ALL,
        }


class ClientQueryResource(ModelResource):
    server_query = fields.ForeignKey(ServerQueryResource, 'server_query')

    class Meta:
        queryset = ClientQuery.objects.all()
        resource_name = 'client_query'
        authorization = Authorization()
        filtering = {
            'path': ALL_WITH_RELATIONS,
        }


class RegionResource(ModelResource):
    query = fields.ForeignKey(ServerQueryResource, 'query')
    block = fields.ForeignKey(BlockResource, 'block')

    class Meta:
        queryset = Region.objects.all()
        resource_name = 'region'
        authorization = Authorization()
        filtering = {
            'query': ALL_WITH_RELATIONS,
        }


class ViewResource(ModelResource):
    server_query = fields.ForeignKey(ServerQueryResource, 'server_query')
    region = fields.ForeignKey(RegionResource, 'region')

    class Meta:
        queryset = View.objects.all()
        resource_name = 'view'
        authorization = Authorization()
        filtering = {
            'query': ALL_WITH_RELATIONS,
        }
