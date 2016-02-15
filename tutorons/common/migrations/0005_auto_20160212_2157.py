# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_viewedregion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewedregion',
            name='time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
