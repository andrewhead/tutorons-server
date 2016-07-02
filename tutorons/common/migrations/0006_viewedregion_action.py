# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20160212_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewedregion',
            name='action',
            field=models.CharField(max_length=6, null=True, blank=True),
        ),
    ]
