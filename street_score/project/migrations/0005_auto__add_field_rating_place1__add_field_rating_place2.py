# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Rating.place1'
        db.add_column('project_rating', 'place1', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['project.Place']), keep_default=False)

        # Adding field 'Rating.place2'
        db.add_column('project_rating', 'place2', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['project.Place']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Rating.place1'
        db.delete_column('project_rating', 'place1_id')

        # Deleting field 'Rating.place2'
        db.delete_column('project_rating', 'place2_id')


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
            'block1_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'block2_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'criterion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['project.Criterion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['project.Place']"}),
            'place2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['project.Place']"}),
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
