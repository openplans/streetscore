import os

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'street_score'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
