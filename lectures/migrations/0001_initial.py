# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=256)),
                ('duration', models.PositiveIntegerField(choices=[(5, 5), (15, 15), (20, 20), (25, 25), (30, 30), (100, 'inne')])),
                ('abstract', models.TextField(max_length=768)),
                ('info', models.TextField(blank=True, max_length=2048)),
                ('type', models.IntegerField(verbose_name='Typ zajęć', choices=[(0, 'Wykład'), (1, 'Warsztaty')], default=0)),
                ('person_type', models.IntegerField(verbose_name='Typ wykładowcy', choices=[(0, 'Sponsor'), (1, 'Gość'), (2, 'Normalny')], default=2)),
                ('description', models.TextField(verbose_name='Opis', max_length=2048, blank=True)),
                ('author_show', models.CharField(blank=True, max_length=256, null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('for_committe', models.BooleanField(verbose_name='Dla komitetu programowego', default=True)),
                ('accepted', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=99)),
            ],
            options={
                'verbose_name': 'Wykład',
                'ordering': ['order', 'id'],
                'verbose_name_plural': 'Wykłady',
            },
        ),
    ]
