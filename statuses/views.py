from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.custom_mixins import HandleNoPermissionMixin
from django.contrib import messages
from .models import Status
from .forms import StatusForm
from .translations import (
    CREATE_STATUS, CREATE_BUTTON, NOT_AUTHORIZED,
    STATUSES_TITLE, STATUS_CREATED, UPDATE_STATUS, UPDATE_BUTTON,
    STATUS_UPDATED, STATUS_DELETED, DELETE_STATUS, DELETE_BUTTON,
    STATUS_IN_USE)
from task_manager.constants import (TITLE, BUTTON_TEXT, FORM_TEMPLATE)

LOGIN_PATH_NAME = 'login'
STATUSES_LIST = 'statuses:statuses_list'


class StatusesListPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    ListView,
):
    model = Status
    template_name = "statuses/statuses_list.html"
    context_object_name = 'statuses'
    no_permission_url = LOGIN_PATH_NAME
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = STATUSES_TITLE
        return context


class CreateStatusPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    CreateView,
):
    model = Status
    form_class = StatusForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy('statuses:statuses_list')
    success_message = STATUS_CREATED
    no_permission_url = LOGIN_PATH_NAME
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_STATUS
        context[BUTTON_TEXT] = CREATE_BUTTON
        return context


class ChangeStatusPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    UpdateView,
):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_UPDATED
    no_permission_url = LOGIN_PATH_NAME
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = UPDATE_STATUS
        context[BUTTON_TEXT] = UPDATE_BUTTON
        return context


class DeleteStatusPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    DeleteView,
):
    model = Status
    template_name = "delete.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_DELETED
    no_permission_url = LOGIN_PATH_NAME
    error_message = NOT_AUTHORIZED

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, STATUS_IN_USE)
        else:
            super().form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_STATUS
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context
