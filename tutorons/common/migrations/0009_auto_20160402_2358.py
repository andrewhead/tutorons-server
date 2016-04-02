# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20160402_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientquery',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='clientquery',
            name='server_query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.ServerQuery', null=True),
        ),
        migrations.AlterField(
            model_name='clientquery',
            name='start_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='region',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Block', null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.ServerQuery', null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='string',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='view',
            name='action',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='view',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Region', null=True),
        ),
        migrations.AlterField(
            model_name='view',
            name='server_query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.ServerQuery', null=True),
        ),
        migrations.AlterField(
            model_name='view',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
