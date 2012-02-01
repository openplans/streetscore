# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Rating'
        db.create_table('project_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('criterion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['project.Criterion'])),
            ('segment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['project.Segment'])),
            ('block_index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('project', ['Rating'])

        # Adding model 'Criterion'
        db.create_table('project_criterion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prompt', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('project', ['Criterion'])


    def backwards(self, orm):
        
        # Deleting model 'Rating'
        db.delete_table('project_rating')

        # Deleting model 'Criterion'
        db.delete_table('project_criterion')


    models = {
        'project.criterion': {
            'Meta': {'object_name': 'Criterion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.TextField', [], {})
        },
        'project.rating': {
            'Meta': {'object_name': 'Rating'},
            'block_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'criterion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['project.Criterion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'segment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['project.Segment']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'project.segment': {
            'Meta': {'object_name': 'Segment', 'db_table': "u'philly_street_osm_line'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'osm_id'"}),
            'way': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '900913', 'null': 'True'})
        }
    }

    complete_apps = ['project']
