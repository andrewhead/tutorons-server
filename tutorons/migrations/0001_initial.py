# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=200, db_index=True)),
                ('doc_text', models.TextField()),
                ('doc_hash', models.CharField(max_length=200, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('ip_addr', models.GenericIPAddressField(null=True, blank=True)),
                ('path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('node', models.CharField(max_length=400)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('string', models.CharField(max_length=400)),
                ('r_type', models.CharField(max_length=200)),
                ('query', models.ForeignKey(to='tutorons.Query')),
            ],
        ),
    ]
