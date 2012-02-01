# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        segment = orm.Segment.objects.all()[0]

        # Deleting field 'Rating.block_index'
        db.delete_column('project_rating', 'block_index')

        # Deleting field 'Rating.segment'
        db.delete_column('project_rating', 'segment_id')

        # Adding field 'Rating.segment1'
        db.add_column('project_rating', 'segment1', self.gf('django.db.models.fields.related.ForeignKey')(default=segment.pk, related_name='+', to=orm['project.Segment']), keep_default=False)

        # Adding field 'Rating.block_index1'
        db.add_column('project_rating', 'block_index1', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Rating.segment2'
        db.add_column('project_rating', 'segment2', self.gf('django.db.models.fields.related.ForeignKey')(default=segment.pk, related_name='+', to=orm['project.Segment']), keep_default=False)

        # Adding field 'Rating.block_index2'
        db.add_column('project_rating', 'block_index2', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        segment = orm.Segment.objects.all()[0]

        # Adding field 'Rating.block_index'
        db.add_column('project_rating', 'block_index', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Rating.segment'
        db.add_column('project_rating', 'segment', self.gf('django.db.models.fields.related.ForeignKey')(default=segment.pk, related_name='ratings', to=orm['project.Segment']), keep_default=False)

        # Deleting field 'Rating.segment1'
        db.delete_column('project_rating', 'segment1_id')

        # Deleting field 'Rating.block_index1'
        db.delete_column('project_rating', 'block_index1')

        # Deleting field 'Rating.segment2'
        db.delete_column('project_rating', 'segment2_id')

        # Deleting field 'Rating.block_index2'
        db.delete_column('project_rating', 'block_index2')


    models = {
        'project.criterion': {
            'Meta': {'object_name': 'Criterion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.TextField', [], {})
        },
        'project.rating': {
            'Meta': {'object_name': 'Rating'},
            'block_index1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'block_index2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'criterion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['project.Criterion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
