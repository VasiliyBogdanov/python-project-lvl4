from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.constants import BUTTON_TEXT, TITLE, FORM_TEMPLATE
from task_manager.custom_mixins import HandleNoPermissionMixin
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
    extra_context = {
        TITLE: LABELS_TITLE
    }


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
    extra_context = {
        TITLE: CREATE_LABEL,
        BUTTON_TEXT: CREATE_BUTTON
    }


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
    extra_context = {
        TITLE: CHANGE_LABEL,
        BUTTON_TEXT: CHANGE_BUTTON
    }


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
    extra_context = {
        TITLE: DELETE_LABEL,
        BUTTON_TEXT: DELETE_BUTTON
    }

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, LABEL_IN_USE)
        else:
            super(DeleteLabelPage, self).form_valid(form)
        return redirect(self.success_url)
