# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lecture'
        db.create_table(u'lectures_lecture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=3)),
            ('abstract', self.gf('django.db.models.fields.TextField')(max_length=512)),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=2048, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('person_type', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('photo_url', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2048, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Participant'])),
            ('author_show', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('accepted', self.gf('django.db.models.fields.BooleanField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=99)),
        ))
        db.send_create_signal(u'lectures', ['Lecture'])


    def backwards(self, orm):
        # Deleting model 'Lecture'
        db.delete_table(u'lectures_lecture')


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
        u'lectures.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'accepted': ('django.db.models.fields.BooleanField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Participant']"}),
            'author_show': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '99'}),
            'person_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'photo_url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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

    complete_apps = ['lectures']