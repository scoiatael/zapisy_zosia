# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Blog Entry',
                'verbose_name_plural': 'Blog Entries',
            },
        ),
    ]
