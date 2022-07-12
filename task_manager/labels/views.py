from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from task_manager.custom_mixins import HandleNoPermissionMixin
from task_manager.constants import BUTTON_TEXT, TITLE, FORM_TEMPLATE
from .forms import LabelForm
from .models import Label
from .translations import (
    NOT_AUTHORIZED, LABELS_TITLE, LABEL_CREATED, CREATE_BUTTON, CREATE_LABEL,
    LABEL_CHANGED, CHANGE_BUTTON, CHANGE_LABEL, LABEL_DELETED, LABEL_IN_USE,
    DELETE_LABEL, DELETE_BUTTON)

LABELS = 'labels'
LOGIN = 'login'
LABELS_LIST = 'labels:labels_list'


class LabelsListPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    ListView,
):
    model = Label
    template_name = "labels/labels_list.html"
    context_object_name = LABELS
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = LABELS_TITLE
        return context


class CreateLabelPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    CreateView,
):
    model = Label
    form_class = LabelForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_CREATED
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_LABEL
        context[BUTTON_TEXT] = CREATE_BUTTON
        return context


class ChangeLabelPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    UpdateView,
):
    model = Label
    form_class = LabelForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_CHANGED
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CHANGE_LABEL
        context[BUTTON_TEXT] = CHANGE_BUTTON
        return context


class DeleteLabelPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    DeleteView,
):
    model = Label
    template_name = "delete.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_DELETED
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, LABEL_IN_USE)
        else:
            super(DeleteLabelPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_LABEL
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context
