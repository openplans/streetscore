# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Rating.score'
        db.alter_column('project_rating', 'score', self.gf('django.db.models.fields.IntegerField')())


    def backwards(self, orm):
        
        # Changing field 'Rating.score'
        db.alter_column('project_rating', 'score', self.gf('django.db.models.fields.PositiveIntegerField')())


    models = {
        'project.criterion': {
            'Meta': {'object_name': 'Criterion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.TextField', [], {})
        },
        'project.rating': {
            'Meta': {'object_name': 'Rating'},
            'block1_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'block2_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'criterion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['project.Criterion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'segment1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['project.Segment']"}),
            'segment2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['project.Segment']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'project.segment': {
            'Meta': {'object_name': 'Segment', 'db_table': "u'philly_street_osm_line'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'osm_id'"}),
            'way': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '900913', 'null': 'True'})
        }
    }

    complete_apps = ['project']
