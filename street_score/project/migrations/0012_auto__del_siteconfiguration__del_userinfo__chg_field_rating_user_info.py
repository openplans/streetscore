# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting model 'SiteConfiguration'
#        db.delete_table('project_siteconfiguration')

        # Deleting model 'UserInfo'
#        db.delete_table('project_userinfo')

        # Changing field 'Rating.user_info'
#        db.alter_column('project_rating', 'user_info_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sessions.UserInfo']))

        db.add_column('project_siteconfiguration', 'about_text_is_html', models.BooleanField(blank=True, default=False))


    def backwards(self, orm):

        # Adding model 'SiteConfiguration'
#        db.create_table('project_siteconfiguration', (
#            ('google_analytics_key', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
#            ('addthis_key', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
#            ('about_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
#            ('addthis_title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
#            ('about_title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
#            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
#            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
#        ))
#        db.send_create_signal('project', ['SiteConfiguration'])

        # Adding model 'UserInfo'
#        db.create_table('project_userinfo', (
#            ('location_source', self.gf('django.db.models.fields.CharField')(max_length=32)),
#            ('lat', self.gf('django.db.models.fields.FloatField')(null=True)),
#            ('session', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sessions.Session'], unique=True)),
#            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
#            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
#            ('lon', self.gf('django.db.models.fields.FloatField')(null=True)),
#            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
#            ('location_data', self.gf('django.db.models.fields.CharField')(max_length=2048)),
#        ))
#        db.send_create_signal('project', ['UserInfo'])

        # Changing field 'Rating.user_info'
#        db.alter_column('project_rating', 'user_info_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['project.UserInfo']))

        db.delete_column('project_siteconfiguration', 'about_text_is_html')


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
            'user_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'null': 'True', 'to': "orm['sessions.UserInfo']"})
        },
        'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        'sessions.userinfo': {
            'Meta': {'object_name': 'UserInfo', 'db_table': "'project_userinfo'"},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'location_data': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'location_source': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'session': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sessions.Session']", 'unique': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['project']
