# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SiteConfiguration'
        db.create_table('project_siteconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('google_analytics_key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('addthis_key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('addthis_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('about_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('about_text', self.gf('django.db.models.fields.TextField')()),
            ('locate_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('locate_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('project', ['SiteConfiguration'])


    def backwards(self, orm):
        
        # Deleting model 'SiteConfiguration'
        db.delete_table('project_siteconfiguration')


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
            'user_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'null': 'True', 'to': "orm['project.UserInfo']"})
        },
        'project.siteconfiguration': {
            'Meta': {'object_name': 'SiteConfiguration'},
            'about_text': ('django.db.models.fields.TextField', [], {}),
            'about_title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'addthis_key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'addthis_title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'google_analytics_key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locate_text': ('django.db.models.fields.TextField', [], {}),
            'locate_title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'})
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
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['project']
