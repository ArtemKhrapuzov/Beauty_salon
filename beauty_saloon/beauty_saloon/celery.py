import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_saloon.settings')

app = Celery('beauty_saloon')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'send-email': {
#         'task': 'users.tasks.send_email',
#         'schedule': crontab(minute='0', hour='*/1'),
#     },
# }
