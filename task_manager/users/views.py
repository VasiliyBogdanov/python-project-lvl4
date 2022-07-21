from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.constants import (TITLE, BUTTON_TEXT, FORM_TEMPLATE)
from task_manager.custom_mixins import HandleNoPermissionMixin
from .forms import CreateUserForm
from .translations import (CREATE_USER, DELETE, DELETE_USER,
                           NO_PERMISSION_TO_MODIFY, REGISTER, UPDATE,
                           USER_IN_USE, UPDATE_USER, USER_DELETED, USERS,
                           USER_CREATED, USER_UPDATED)

USERS_LIST_NAME = 'users:users_list'
LOGIN_NAME = 'login'
USERS_CONTEXT_NAME = 'users'
USERS_TEMPLATE_PATH = "users/users.html"
DELETE_TEMPLATE_PATH = "delete.html"


class UserListView(ListView):
    model = get_user_model()
    template_name = USERS_TEMPLATE_PATH
    context_object_name = USERS_CONTEXT_NAME
    extra_context = {TITLE: USERS}


class CreateUserView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = FORM_TEMPLATE
    form_class = CreateUserForm
    success_url = reverse_lazy(LOGIN_NAME)
    success_message = USER_CREATED
    extra_context = {
        TITLE: CREATE_USER,
        BUTTON_TEXT: REGISTER
    }


class ChangeUser(
    LoginRequiredMixin,
        SuccessMessageMixin,
        HandleNoPermissionMixin,
        UserPassesTestMixin,
        UpdateView):
    model = get_user_model()
    template_name = FORM_TEMPLATE
    form_class = CreateUserForm
    success_message = USER_UPDATED
    success_url = reverse_lazy(USERS_LIST_NAME)
    no_permission_url = reverse_lazy(USERS_LIST_NAME)
    error_message = NO_PERMISSION_TO_MODIFY
    extra_context = {
        TITLE: UPDATE_USER,
        BUTTON_TEXT: UPDATE
    }

    def test_func(self):
        return self.request.user == self.get_object()


class DeleteUser(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = get_user_model()
    template_name = DELETE_TEMPLATE_PATH
    success_url = reverse_lazy(USERS_LIST_NAME)
    success_message = USER_DELETED
    no_permission_url = reverse_lazy(USERS_LIST_NAME)
    error_message = NO_PERMISSION_TO_MODIFY
    extra_context = {
        TITLE: DELETE_USER,
        BUTTON_TEXT: DELETE
    }

    def test_func(self):
        return self.request.user == self.get_object()

    def form_valid(self, form):
        if self.get_object().tasks.all() or self.get_object().objectives.all():
            messages.error(self.request, USER_IN_USE)
        else:
            super().form_valid(form)
        return redirect(USERS_LIST_NAME)
