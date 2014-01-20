# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Sponsor', fields ['name']
        db.create_unique(u'sponsors_sponsor', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Sponsor', fields ['name']
        db.delete_unique(u'sponsors_sponsor', ['name'])


    models = {
        u'sponsors.sponsor': {
            'Meta': {'ordering': "['order', 'id']", 'object_name': 'Sponsor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        }
    }

    complete_apps = ['sponsors']