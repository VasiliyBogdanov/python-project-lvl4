from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, UpdateView,
                                  DetailView)
from django_filters.views import FilterView

from task_manager.constants import (FORM_TEMPLATE, TITLE, BUTTON_TEXT)
from task_manager.custom_mixins import HandleNoPermissionMixin
from task_manager.users.models import User
from .forms import TaskForm, TaskFilter
from .models import Task
from .translations import (
    NOT_AUTHORIZED, TASKS_TITLE, TASKS_BUTTON, TASK_CREATED, CREATE_TASK,
    CREATE_BUTTON, TASK_UPDATED, UPDATE_BUTTON, UPDATE_TASK, TASK_DELETED,
    BY_AUTHOR, DELETE_TASK, DELETE_BUTTON, TASK_VIEW)

TASKS = 'tasks'
LOGIN = 'login'
TASKS_LIST = 'tasks:tasks_list'
LABELS = 'labels'


class TasksListPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    FilterView,
):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = TASKS
    filterset_class = TaskFilter
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED
    extra_context = {
        TITLE: TASKS_TITLE,
        BUTTON_TEXT: TASKS_BUTTON
    }


class CreateTaskPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    CreateView,
):

    model = Task
    form_class = TaskForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_CREATED
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED
    extra_context = {
        TITLE: CREATE_TASK,
        BUTTON_TEXT: CREATE_BUTTON
    }

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class ChangeTaskPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    UpdateView,
):
    model = Task
    form_class = TaskForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_UPDATED
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED
    extra_context = {
        TITLE: UPDATE_TASK,
        BUTTON_TEXT: UPDATE_BUTTON
    }


class DeleteTaskPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    DeleteView,
):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_DELETED
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED
    extra_context = {
        TITLE: DELETE_TASK,
        BUTTON_TEXT: DELETE_BUTTON
    }

    def form_valid(self, form):
        if self.request.user == self.get_object().author:
            super().form_valid(form)
        else:
            messages.error(self.request, BY_AUTHOR)
        return redirect(self.success_url)


class TaskDetailPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    DetailView,
):
    model = Task
    template_name = "tasks/tasks_details.html"
    context_object_name = 'task'
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context[TITLE] = TASK_VIEW
        context[LABELS] = self.get_object().labels.all()
        return context
