from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from .tasks import send_email
from users.forms import RegisterUserForm, LoginUserForm
from users.forms import UserCreationForm, AuthenticationForm
from users.utils import send_email_for_verify

User = get_user_model()


class MyLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'service/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


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
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class RegisterUser(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': RegisterUserForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            #send_email_for_verify(request, user)
            #params = request.GET.urlencode()
            send_email.delay(user.id)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


# class LoginUser(LoginView):
#     """Форма авторизации"""
#     forms_class = LoginUserForm
#     template_name = 'service/login.html'
#
#     def get_success_url(self):
#         return reverse_lazy('home')


def logout_user(request):
    """Выход из авторизации"""
    logout(request)
    return redirect('login')
