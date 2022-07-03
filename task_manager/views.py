from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


def index(request):
    return render(request, "index.html")


class LoginPage(SuccessMessageMixin, LoginView):
    template_name = "form.html"
    success_message = _('You are logged in')
    next_page = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Log in'
        context['title'] = _("Login")
        return context


class LogoutPage(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
