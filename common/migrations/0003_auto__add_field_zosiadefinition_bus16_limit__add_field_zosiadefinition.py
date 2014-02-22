# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ZosiaDefinition.bus16_limit'
        db.add_column(u'common_zosiadefinition', 'bus16_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=48),
                      keep_default=False)

        # Adding field 'ZosiaDefinition.bus18_limit'
        db.add_column(u'common_zosiadefinition', 'bus18_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=48),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ZosiaDefinition.bus16_limit'
        db.delete_column(u'common_zosiadefinition', 'bus16_limit')

        # Deleting field 'ZosiaDefinition.bus18_limit'
        db.delete_column(u'common_zosiadefinition', 'bus18_limit')


    models = {
        u'common.zosiadefinition': {
            'Meta': {'object_name': 'ZosiaDefinition'},
            'account_data_1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_data_2': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_data_3': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'active_definition': ('django.db.models.fields.BooleanField', [], {}),
            'bus16_limit': ('django.db.models.fields.IntegerField', [], {'default': '48'}),
            'bus18_limit': ('django.db.models.fields.IntegerField', [], {'default': '48'}),
            'bus_limit': ('django.db.models.fields.IntegerField', [], {'default': '98'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'city_c': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'city_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'hotel': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hotel_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lectures_suggesting_final': ('django.db.models.fields.DateTimeField', [], {}),
            'lectures_suggesting_start': ('django.db.models.fields.DateTimeField', [], {}),
            'payment_deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'price_organization': ('django.db.models.fields.IntegerField', [], {}),
            'price_overnight': ('django.db.models.fields.IntegerField', [], {}),
            'price_overnight_breakfast': ('django.db.models.fields.IntegerField', [], {}),
            'price_overnight_dinner': ('django.db.models.fields.IntegerField', [], {}),
            'price_overnight_full': ('django.db.models.fields.IntegerField', [], {}),
            'price_transport': ('django.db.models.fields.IntegerField', [], {}),
            'registration_final': ('django.db.models.fields.DateTimeField', [], {}),
            'registration_start': ('django.db.models.fields.DateTimeField', [], {}),
            'rooming_final': ('django.db.models.fields.DateTimeField', [], {}),
            'rooming_start': ('django.db.models.fields.DateTimeField', [], {}),
            'zosia_final': ('django.db.models.fields.DateTimeField', [], {}),
            'zosia_start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['common']