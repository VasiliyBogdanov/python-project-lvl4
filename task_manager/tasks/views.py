from task_manager.constants import (FORM_TEMPLATE, TITLE, BUTTON_TEXT)
from .translations import (
    NOT_AUTHORIZED, TASKS_TITLE, TASKS_BUTTON, TASK_CREATED, CREATE_TASK,
    CREATE_BUTTON, TASK_UPDATED, UPDATE_BUTTON, UPDATE_TASK, TASK_DELETED,
    BY_AUTHOR, DELETE_TASK, DELETE_BUTTON, TASK_VIEW)
from .forms import TaskForm, TaskFilter
from task_manager.users.models import User
from .models import Task
from django.shortcuts import redirect
from django.contrib import messages
from task_manager.custom_mixins import HandleNoPermissionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, DeleteView, UpdateView,
                                  DetailView)
from django_filters.views import FilterView

TASKS = 'tasks'
LOGIN = 'login'
TASKS_LIST = 'tasks:tasks_list'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = TASKS_TITLE
        context[BUTTON_TEXT] = TASKS_BUTTON
        return context


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

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_TASK
        context[BUTTON_TEXT] = CREATE_BUTTON
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = UPDATE_TASK
        context[BUTTON_TEXT] = UPDATE_BUTTON
        return context


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

    def form_valid(self, form):
        if self.request.user == self.get_object().author:
            super().form_valid(form)
        else:
            messages.error(self.request, BY_AUTHOR)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_TASK
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context


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
        context['labels'] = self.get_object().labels.all()
        return context
