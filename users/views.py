from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .forms import CreateUserForm
from django.urls import reverse_lazy
from .custom_mixins import HandleNoPermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from .translations import (CHANGE_USER, CREATE_USER, DELETE, DELETE_USER,
                           NO_PERMISSION_TO_MODIFY, REGISTER, UPDATE,
                           USER_DELETED, USERS, USER_CREATED, USER_UPDATED)
# Create your views here.
TITLE = 'title'
BUTTON_TEXT = 'button_text'

USERS_LIST_NAME = 'users:users_list'
LOGIN_NAME = 'login'
USERS_CONTEXT_NAME = 'users'

USERS_TEMPLATE_PATH = "users/users.html"
FORM_TEMPLATE_PATH = 'form.html'
DELETE_TEMPLATE_PATH = "delete.html"


class UserListView(ListView):
    model = get_user_model()
    template_name = USERS_TEMPLATE_PATH
    context_object_name = USERS_CONTEXT_NAME

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = USERS
        return context


class CreateUserView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = FORM_TEMPLATE_PATH
    form_class = CreateUserForm
    success_url = reverse_lazy(LOGIN_NAME)
    success_message = USER_CREATED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_USER
        context[BUTTON_TEXT] = REGISTER
        return context


class ChangeUser(
    LoginRequiredMixin,
        SuccessMessageMixin,
        HandleNoPermissionMixin,
        UserPassesTestMixin,
        UpdateView):
    model = get_user_model()
    template_name = FORM_TEMPLATE_PATH
    form_class = CreateUserForm
    success_message = USER_UPDATED
    success_url = reverse_lazy(USERS_LIST_NAME)
    no_permission_url = reverse_lazy(USERS_LIST_NAME)
    error_message = NO_PERMISSION_TO_MODIFY

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CHANGE_USER
        context[BUTTON_TEXT] = UPDATE
        return context


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

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_USER
        context[BUTTON_TEXT] = DELETE
        return context

    def form_valid(self, form):
        super(DeleteUser, self).form_valid(form)
        return redirect(USERS_LIST_NAME)
