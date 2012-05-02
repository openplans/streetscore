# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Rating.user_info'
        db.add_column('project_rating', 'user_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.UserInfo'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Rating.user_info'
        db.delete_column('project_rating', 'user_info_id')


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
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.UserInfo']", 'null': 'True'})
        },
        'project.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'location_data': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'location_source': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'session': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sessions.Session']", 'unique': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['project']
