# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'rooms_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=1)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('short_unlock_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'rooms', ['Room'])

        # Adding model 'UserInRoom'
        db.create_table(u'rooms_userinroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Participant'], unique=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rooms.Room'])),
            ('ownership', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'rooms', ['UserInRoom'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'rooms_room')

        # Deleting model 'UserInRoom'
        db.delete_table(u'rooms_userinroom')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'rooms.room': {
            'Meta': {'object_name': 'Room'},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'short_unlock_time': ('django.db.models.fields.DateTimeField', [], {}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Participant']", 'through': u"orm['rooms.UserInRoom']", 'symmetrical': 'False'})
        },
        u'rooms.userinroom': {
            'Meta': {'ordering': "['locator__last_name', 'locator__first_name']", 'object_name': 'UserInRoom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Participant']", 'unique': 'True'}),
            'ownership': ('django.db.models.fields.BooleanField', [], {}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rooms.Room']"})
        },
        u'users.participant': {
            'Meta': {'object_name': 'Participant'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.TextField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.TextField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['rooms']