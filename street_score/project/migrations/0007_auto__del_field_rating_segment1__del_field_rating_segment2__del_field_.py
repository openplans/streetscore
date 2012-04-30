# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Rating.segment1'
        db.delete_column('project_rating', 'segment1_id')

        # Deleting field 'Rating.segment2'
        db.delete_column('project_rating', 'segment2_id')

        # Deleting field 'Rating.block1_index'
        db.delete_column('project_rating', 'block1_index')

        # Deleting field 'Rating.block2_index'
        db.delete_column('project_rating', 'block2_index')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Rating.segment1'
        raise RuntimeError("Cannot reverse this migration. 'Rating.segment1' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Rating.segment2'
        raise RuntimeError("Cannot reverse this migration. 'Rating.segment2' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Rating.block1_index'
        raise RuntimeError("Cannot reverse this migration. 'Rating.block1_index' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Rating.block2_index'
        raise RuntimeError("Cannot reverse this migration. 'Rating.block2_index' and its values cannot be restored.")


    models = {
        'project.criterion': {
            'Meta': {'object_name': 'Criterion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.TextField', [], {})
        },
        'project.place': {
            'Meta': {'object_name': 'Place'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {})
        },
        'project.rating': {
            'Meta': {'object_name': 'Rating'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'criterion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['project.Criterion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['project.Place']"}),
            'place2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['project.Place']"}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'project.segment': {
            'Meta': {'object_name': 'Segment', 'db_table': "u'philly_street_osm_line'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'osm_id'"}),
            'way': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '900913', 'null': 'True'})
        }
    }

    complete_apps = ['project']
