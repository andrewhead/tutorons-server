from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Block(models.Model):
    ''' A version of a webpage at a specific point in time'''
    time = models.DateTimeField(auto_now_add=True)

    url = models.CharField(db_index=True, max_length=200)
    block_type = models.CharField(max_length=100)
    block_text = models.TextField()
    block_hash = models.IntegerField()

    def __str__(self):
        return "URL: %s, Type:%s, Time:%s, Hash:%d" % (
            self.url,
            self.block_type,
            self.time,
            self.block_hash)


@python_2_unicode_compatible
class ServerQuery(models.Model):
    '''Server view of a request to get regions for a document'''
    start_time = models.DateTimeField(auto_now_add=True)

    end_time = models.DateTimeField(null=True, blank=True, auto_now=True)
    ip_addr = models.GenericIPAddressField(blank=True, null=True)
    path = models.CharField(max_length=100)

    def __str__(self):
        return "Time:%s, IP:%s, Path:%s" % (
            self.start_time,
            self.ip_addr,
            self.path)


@python_2_unicode_compatible
class ClientQuery(models.Model):
    '''Client view of a request to get regions for a document'''
    start_time = models.DateTimeField(null=True, blank=True, auto_now_add=False)
    end_time = models.DateTimeField(null=True, blank=True, auto_now_add=False)
    server_query = models.ForeignKey(ServerQuery, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Start:%s, End:%s, Query:%s" % (
            self.start_time,
            self.end_time,
            self.server_query)


@python_2_unicode_compatible
class Region(models.Model):
    '''An explainable region of text'''
    query = models.ForeignKey(ServerQuery, on_delete=models.CASCADE, null=True, blank=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True, auto_now_add=False)
    end_time = models.DateTimeField(null=True, blank=True, auto_now_add=False)

    node = models.CharField(max_length=1000)
    start = models.IntegerField()
    end = models.IntegerField()
    string = models.CharField(max_length=400)
    r_type = models.CharField(max_length=100)
    r_method = models.CharField(max_length=100)

    def __str__(self):
        return "Node: %s, Start:%d, End:%d, String:%s, Type:%s, Method:%s" % (
            self.node,
            self.start,
            self.end,
            self.string,
            self.r_type,
            self.r_method)


@python_2_unicode_compatible
class ViewedRegion(models.Model):
    '''Client view of a request to get regions for a document'''
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    server_query = models.ForeignKey(ServerQuery, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return "Region ID:%s, ServerQuery ID:%s, Time:%s" % (
            self.region,
            self.server_query,
            self.time)
