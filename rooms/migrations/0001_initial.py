# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('number', models.CharField(max_length=16)),
                ('capacity', models.PositiveIntegerField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(max_length=16)),
                ('hidden', models.BooleanField(default=False)),
                ('short_unlock_time', models.DateTimeField()),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='UserInRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ownership', models.BooleanField()),
            ],
            options={
                'ordering': ['locator__last_name', 'locator__first_name'],
            },
        ),
    ]
