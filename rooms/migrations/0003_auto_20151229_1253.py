# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20150902_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='short_unlock_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
