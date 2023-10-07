from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from users.forms import RegisterUserForm, LoginUserForm


class RegisterUser(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': RegisterUserForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


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
