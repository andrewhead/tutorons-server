# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20160402_2210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='r_method',
            new_name='region_method',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='r_type',
            new_name='region_type',
        ),
    ]
