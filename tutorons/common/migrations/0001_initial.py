# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=200, db_index=True)),
                ('block_type', models.CharField(max_length=100)),
                ('block_text', models.TextField()),
                ('block_hash', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ClientQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('node', models.CharField(max_length=1000)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('string', models.CharField(max_length=400)),
                ('r_type', models.CharField(max_length=100)),
                ('r_method', models.CharField(max_length=100)),
                ('block', models.ForeignKey(blank=True, to='common.Block', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True, null=True)),
                ('ip_addr', models.GenericIPAddressField(null=True, blank=True)),
                ('path', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='region',
            name='query',
            field=models.ForeignKey(blank=True, to='common.ServerQuery', null=True),
        ),
        migrations.AddField(
            model_name='clientquery',
            name='server_query',
            field=models.ForeignKey(blank=True, to='common.ServerQuery', null=True),
        ),
    ]
