# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ZosiaDefinition'
        db.create_table('common_zosiadefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active_definition', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('registration_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('registration_final', self.gf('django.db.models.fields.DateTimeField')()),
            ('payment_deadline', self.gf('django.db.models.fields.DateTimeField')()),
            ('lectures_suggesting_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('lectures_suggesting_final', self.gf('django.db.models.fields.DateTimeField')()),
            ('rooming_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('rooming_final', self.gf('django.db.models.fields.DateTimeField')()),
            ('zosia_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('zosia_final', self.gf('django.db.models.fields.DateTimeField')()),
            ('price_overnight', self.gf('django.db.models.fields.IntegerField')()),
            ('price_overnight_breakfast', self.gf('django.db.models.fields.IntegerField')()),
            ('price_overnight_dinner', self.gf('django.db.models.fields.IntegerField')()),
            ('price_overnight_full', self.gf('django.db.models.fields.IntegerField')()),
            ('price_transport', self.gf('django.db.models.fields.IntegerField')()),
            ('price_organization', self.gf('django.db.models.fields.IntegerField')()),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('account_data_1', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('account_data_2', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('account_data_3', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city_c', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('hotel', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('hotel_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('common', ['ZosiaDefinition'])


    def backwards(self, orm):
        # Deleting model 'ZosiaDefinition'
        db.delete_table('common_zosiadefinition')


    models = {
        'common.zosiadefinition': {
            'Meta': {'object_name': 'ZosiaDefinition'},
            'account_data_1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_data_2': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_data_3': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'active_definition': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'city_c': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'city_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'hotel': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hotel_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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