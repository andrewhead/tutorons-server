# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20160208_0000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='time',
            new_name='created_time',
        ),
    ]
