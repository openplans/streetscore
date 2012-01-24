import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'street_score.project.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
