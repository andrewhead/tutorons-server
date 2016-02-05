# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorons', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.RemoveField(
            model_name='region',
            name='query',
        ),
        migrations.DeleteModel(
            name='Query',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]
