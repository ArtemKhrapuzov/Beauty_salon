from django.shortcuts import render
from django.views.generic import ListView

from service.models import *


class MainListView(ListView):

    template_name = 'service/index.html'

def index(request):
    return render(request, 'service/index.html')
