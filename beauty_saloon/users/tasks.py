from django.contrib.auth import get_user_model

from beauty_saloon.celery import app

from .utils import send_email_for_verify

User = get_user_model()


@app.task()
def send_email(user_id):
    send_email_for_verify(User.objects.get(id=user_id))


#celery -A beauty_saloon worker -l info -P gevent

