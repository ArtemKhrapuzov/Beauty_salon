from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator as \
    token_generator

from users.forms import RegisterUserForm
from users.utils import send_email_for_verify

User = get_user_model()


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class RegisterUser(View):
    """Регистрация пользователя"""
    template_name = 'registration/register.html'

    def get(self, request):
        """Отображение формы регистрации"""
        context = {
            'form': RegisterUserForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Подтверждение почты"""
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def logout_user(request):
    """Выход из авторизации"""
    logout(request)
    return redirect('login')


def agree(request):
    """Пользовательское соглашение"""
    return render(request, 'registration/agree.html')
