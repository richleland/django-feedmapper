# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Mapping'
        db.create_table('feedmapper_mapping', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parser', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('purge', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data_map', self.gf('django.db.models.fields.TextField')(default='{}')),
            ('notification_recipients', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parse_attempted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('parse_succeeded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parse_log', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('feedmapper', ['Mapping'])


    def backwards(self, orm):
        
        # Deleting model 'Mapping'
        db.delete_table('feedmapper_mapping')


    models = {
        'feedmapper.mapping': {
            'Meta': {'object_name': 'Mapping'},
            'data_map': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notification_recipients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parse_attempted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'parse_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parse_succeeded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parser': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'purge': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['feedmapper']
