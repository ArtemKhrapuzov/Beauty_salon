from django.contrib.auth import get_user_model

from beauty_saloon.celery import app

from .utils import send_email_for_verify

User = get_user_model()


@app.task()
def send_email(request, user_id):
    #params = request.GET.urlencode()
    send_email_for_verify(request, user_id)
