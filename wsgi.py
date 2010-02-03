import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(PROJECT_ROOT, 'server'))
sys.path.append(os.path.join(PROJECT_ROOT, 'third_party'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'minutiae.settings.live'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
