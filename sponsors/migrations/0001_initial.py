# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=255, unique=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(upload_to='img')),
                ('order', models.IntegerField(default=100)),
            ],
            options={
                'verbose_name': 'sponsor',
                'ordering': ['order', 'id'],
                'verbose_name_plural': 'sponsorzy',
            },
        ),
    ]
