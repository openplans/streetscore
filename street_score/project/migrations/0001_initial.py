# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Answer'
        db.create_table('street_score_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['street_score.Question'])),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('street_score', ['Answer'])

        # Adding model 'Question'
        db.create_table('street_score_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prompt', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('street_score', ['Question'])


    def backwards(self, orm):
        
        # Deleting model 'Answer'
        db.delete_table('street_score_answer')

        # Deleting model 'Question'
        db.delete_table('street_score_question')


    models = {
        'street_score.answer': {
            'Meta': {'object_name': 'Answer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['street_score.Question']"}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'street_score.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['street_score']
