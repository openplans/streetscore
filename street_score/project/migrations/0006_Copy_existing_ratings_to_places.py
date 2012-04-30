# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


#
# The following two constructs will be useful when converting existing ratings
# identified by blocks to ratings identified by places.
#

def blocks(self):
    """
    The blocks that fall along the segment.  If the segment is shorter than
    the block length, it will contain only one block.
    """
    class BlockSet (object):
        def __init__(self, segment):
            self.segment = segment

        def __len__(self):
            return int(math.ceil(self.segment.way.length / Block.MAX_LENGTH))

        def __getitem__(self, n):
            return Block(self.segment, n)

    return BlockSet(self)


class Block (object):
    MAX_LENGTH = 200.0

    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    @property
    def _start_interpolation(self):
        return (self.MAX_LENGTH * self.index) / self.segment.way.length

    @property
    def length(self):
        return min(self.segment.length - (self.index * self.MAX_LENGTH), self.MAX_LENGTH)

    @property
    def characteristic_point(self):
        """
        The a point that will represent the block (not necessarily uniquely).
        """
        point_data = Segment.objects.raw(
            ('SELECT *, ST_transform(ST_line_interpolate_point(way, %s), 4326) '
                 'AS q_start_point '
             'FROM philly_street_osm_line WHERE osm_id=%s'),
            [self._start_interpolation, self.segment.id])[0].q_start_point
        point = GEOSGeometry(point_data)
        return point


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."


    def backwards(self, orm):
        "Write your backwards methods here."


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
