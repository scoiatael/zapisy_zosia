# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='tytuł', max_length=255)),
                ('description', models.TextField(verbose_name='opis', null=True, blank=True)),
                ('created', models.TimeField(auto_now_add=True)),
                ('edited', models.TimeField(auto_now=True)),
                ('time_start', models.DateTimeField(verbose_name='Początek', null=True, blank=True)),
                ('time_end', models.DateTimeField(verbose_name='Koniec', null=True, blank=True)),
                ('only_bus', models.BooleanField(verbose_name='Tylko dla jadących autokarem', default=False)),
                ('visible', models.BooleanField(verbose_name='Widoczna', default=False)),
            ],
            options={
                'verbose_name': 'Ankieta',
                'verbose_name_plural': 'Ankiety',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('question', models.CharField(verbose_name='Pytanie', max_length=255)),
                ('order', models.IntegerField(default=100)),
            ],
            options={
                'verbose_name': 'Pytanie',
                'ordering': ['order', 'id'],
                'verbose_name_plural': 'Pytanie',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.TimeField(auto_now_add=True)),
                ('edited', models.TimeField(auto_now=True)),
                ('question', models.ForeignKey(verbose_name='pytanie', to='polls.Question')),
            ],
            options={
                'verbose_name': 'Odpowiedź',
                'verbose_name_plural': 'Odpowiedzi',
            },
        ),
    ]
