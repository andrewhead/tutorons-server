# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20160208_0129'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewedRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('region', models.ForeignKey(blank=True, to='common.Region', null=True)),
                ('server_query', models.ForeignKey(blank=True, to='common.ServerQuery', null=True)),
            ],
        ),
    ]
