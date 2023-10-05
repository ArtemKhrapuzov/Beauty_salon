from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from service.forms import RegisterUserForm, LoginUserForm


# class MainListView(ListView):
#     template_name = 'service/index.html'

def index(request):
    return render(request, 'service/index.html')


class RegisterUser(CreateView):
    """Форма регистрации"""
    form_class = RegisterUserForm
    template_name = 'service/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """При успешной регистрации, переводит на главную страницу"""
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    """Форма авторизации"""
    forms_class = LoginUserForm
    template_name = 'service/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    """Выход из авторизации"""
    logout(request)
    return redirect('login')


