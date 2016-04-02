from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Block(models.Model):
    ''' A block of a web page in which an explainable region was found. '''

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
    ''' A query made to this server. '''

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
    ''' The timing of a request to this server from the client's perspctive. '''

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
    ''' An explainable segment of text from a webpage. '''

    query = models.ForeignKey(ServerQuery, on_delete=models.CASCADE, null=True, blank=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

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
class View(models.Model):
    ''' The act of a user viewing or closing an explanation. '''

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    server_query = models.ForeignKey(ServerQuery, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True, auto_now=True)
    action = models.CharField(null=True, blank=True, max_length=6)

    def __str__(self):
        return "Region ID:%s, ServerQuery ID:%s, Time:%s" % (
            self.region,
            self.action,
            self.server_query,
            self.time)
