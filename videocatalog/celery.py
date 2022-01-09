import os
from celery import Celery

# 1. Command Line Arguments ( python3 app.py [ .... ] )
# 2. Environment Variables
# 3. Config File
# 4. Interactive

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videocatalog.settings')
app = Celery('videocatalog')
# django.conf:settings -> from django.conf import settings
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
