import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_saloon.settings')

app = Celery('beauty_saloon')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



