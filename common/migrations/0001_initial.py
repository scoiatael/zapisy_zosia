# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZosiaDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('active_definition', models.BooleanField()),
                ('registration_start', models.DateTimeField()),
                ('registration_final', models.DateTimeField()),
                ('registration_limit', models.IntegerField(default=170)),
                ('payment_deadline', models.DateTimeField()),
                ('lectures_suggesting_start', models.DateTimeField()),
                ('lectures_suggesting_final', models.DateTimeField()),
                ('rooming_start', models.DateTimeField()),
                ('rooming_final', models.DateTimeField()),
                ('zosia_start', models.DateTimeField()),
                ('zosia_final', models.DateTimeField()),
                ('bus_limit', models.IntegerField(default=98)),
                ('bus16_limit', models.IntegerField(default=48)),
                ('bus18_limit', models.IntegerField(default=48)),
                ('price_overnight', models.IntegerField()),
                ('price_overnight_breakfast', models.IntegerField()),
                ('price_overnight_dinner', models.IntegerField()),
                ('price_overnight_full', models.IntegerField()),
                ('price_transport', models.IntegerField()),
                ('price_organization', models.IntegerField()),
                ('account_number', models.CharField(max_length=32)),
                ('account_data_1', models.CharField(max_length=40)),
                ('account_data_2', models.CharField(max_length=40)),
                ('account_data_3', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=20)),
                ('city_c', models.CharField(verbose_name='miasto w celowniku', max_length=20)),
                ('city_url', models.URLField()),
                ('hotel', models.CharField(max_length=30)),
                ('hotel_url', models.URLField()),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Ustawienie',
                'verbose_name_plural': 'Ustawienia',
            },
        ),
    ]
