# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, verbose_name='adres email', max_length=254)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('is_active', models.BooleanField(help_text='Oznacza czy użytkownika należy uważać za aktywnego. Odznacz to, zamiast usuwać konta.', default=True, verbose_name='aktywny')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data przyłączenia')),
                ('committee', models.BooleanField(default=False, verbose_name='programme committee')),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, verbose_name='groups', related_name='user_set', to='auth.Group', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', related_name='user_set', to='auth.Permission', related_query_name='user')),
            ],
            options={
                'verbose_name_plural': 'participants',
                'verbose_name': 'participant',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Organizacje',
                'verbose_name': 'Organizacja',
            },
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('day_1', models.BooleanField()),
                ('day_2', models.BooleanField()),
                ('day_3', models.BooleanField()),
                ('breakfast_2', models.BooleanField()),
                ('breakfast_3', models.BooleanField()),
                ('breakfast_4', models.BooleanField()),
                ('dinner_1', models.BooleanField()),
                ('dinner_2', models.BooleanField()),
                ('dinner_3', models.BooleanField()),
                ('bus', models.BooleanField(default=False)),
                ('vegetarian', models.BooleanField()),
                ('paid', models.BooleanField(default=False)),
                ('shirt_size', models.CharField(max_length=5, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')])),
                ('shirt_type', models.CharField(max_length=1, choices=[('m', 'klasyczna'), ('f', 'żeńska')])),
                ('want_bus', models.BooleanField(default=False)),
                ('minutes_early', models.IntegerField(default=0)),
                ('bus_hour', models.CharField(default='', null=True, blank=True, choices=[('', 'obojętne'), ('16:00', '16:00'), ('18:00', '18:00')], max_length=10)),
                ('photo_url', models.CharField(null=True, blank=True, max_length=250)),
                ('description', models.TextField(blank=True, verbose_name='description', max_length=2048)),
                ('org', models.ForeignKey(to='users.Organization')),
                ('state', models.ForeignKey(to='common.ZosiaDefinition')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Preferencje',
            },
        ),
        migrations.CreateModel(
            name='Waiting',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('day_1', models.BooleanField()),
                ('day_2', models.BooleanField()),
                ('day_3', models.BooleanField()),
                ('state', models.ForeignKey(to='common.ZosiaDefinition')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
