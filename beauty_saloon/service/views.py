from django.shortcuts import render


# class MainListView(ListView):
#     template_name = 'service/index.html'

def index(request):
    return render(request, 'service/index.html')
