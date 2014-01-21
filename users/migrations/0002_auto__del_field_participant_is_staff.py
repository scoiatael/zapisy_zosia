# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Participant.is_staff'
        db.delete_column(u'users_participant', 'is_staff')


    def backwards(self, orm):
        # Adding field 'Participant.is_staff'
        db.add_column(u'users_participant', 'is_staff',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'common.zosiadefinition': {
            'Meta': {'object_name': 'ZosiaDefinition'},
            'account_data_1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_data_2': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_data_3': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'active_definition': ('django.db.models.fields.BooleanField', [], {}),
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
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.organization': {
            'Meta': {'object_name': 'Organization'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'})
        },
        u'users.participant': {
            'Meta': {'object_name': 'Participant'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.TextField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.TextField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'users.userpreferences': {
            'Meta': {'object_name': 'UserPreferences'},
            'breakfast_2': ('django.db.models.fields.BooleanField', [], {}),
            'breakfast_3': ('django.db.models.fields.BooleanField', [], {}),
            'breakfast_4': ('django.db.models.fields.BooleanField', [], {}),
            'bus': ('django.db.models.fields.BooleanField', [], {}),
            'bus_hour': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True'}),
            'day_1': ('django.db.models.fields.BooleanField', [], {}),
            'day_2': ('django.db.models.fields.BooleanField', [], {}),
            'day_3': ('django.db.models.fields.BooleanField', [], {}),
            'dinner_1': ('django.db.models.fields.BooleanField', [], {}),
            'dinner_2': ('django.db.models.fields.BooleanField', [], {}),
            'dinner_3': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes_early': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'org': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Organization']"}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shirt_size': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'shirt_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.ZosiaDefinition']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Participant']", 'unique': 'True'}),
            'vegetarian': ('django.db.models.fields.BooleanField', [], {}),
            'want_bus': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['users']