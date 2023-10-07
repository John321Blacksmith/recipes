"""
Initialize a celery istance and define both settings
and a list of tasks the selery workers would perform.
"""
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confs.settings')
app = Celery('confs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()