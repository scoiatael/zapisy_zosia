# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('pub_date', models.DateTimeField()),
                ('content', models.TextField()),
            ],
            options={
                'get_latest_by': 'pub_date',
            },
        ),
    ]