# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_viewedregion_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, null=True)),
                ('action', models.CharField(max_length=6, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='viewedregion',
            name='region',
        ),
        migrations.RemoveField(
            model_name='viewedregion',
            name='server_query',
        ),
        migrations.RemoveField(
            model_name='region',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='region',
            name='start_time',
        ),
        migrations.DeleteModel(
            name='ViewedRegion',
        ),
        migrations.AddField(
            model_name='view',
            name='region',
            field=models.ForeignKey(blank=True, to='common.Region', null=True),
        ),
        migrations.AddField(
            model_name='view',
            name='server_query',
            field=models.ForeignKey(blank=True, to='common.ServerQuery', null=True),
        ),
    ]
