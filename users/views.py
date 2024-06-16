from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


class Login(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('tasks:tasks')


class SignupView(CreateView):
    model = get_user_model()
    form_class = SignupForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tasks:tasks')
        return super().dispatch(request, *args, **kwargs)
