# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Sponsor.logo'
        db.alter_column(u'sponsors_sponsor', 'logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Sponsor.logo'
        db.alter_column(u'sponsors_sponsor', 'logo', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    models = {
        u'sponsors.sponsor': {
            'Meta': {'ordering': "['order', 'id']", 'object_name': 'Sponsor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        }
    }

    complete_apps = ['sponsors']