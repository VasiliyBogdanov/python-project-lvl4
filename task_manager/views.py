from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from task_manager.constants import (FORM_TEMPLATE, TITLE, BUTTON_TEXT)
from .translations import (LOGIN, LOGGED_IN, LOGGED_OUT, LOGIN_BUTTON)

INDEX = 'index'


def index(request):
    return render(request, "index.html")


class LoginPage(SuccessMessageMixin, LoginView):
    template_name = FORM_TEMPLATE
    success_message = LOGGED_IN
    next_page = reverse_lazy(INDEX)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[BUTTON_TEXT] = LOGIN_BUTTON
        context[TITLE] = LOGIN
        return context


class LogoutPage(LogoutView):
    next_page = reverse_lazy(INDEX)

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, LOGGED_OUT)
        return super().dispatch(request, *args, **kwargs)
