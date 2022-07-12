from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from .models import Task
from task_manager.users.models import User
import django_filters
from .translations import (
    NAME_LABEL, DESCRIPTION_LABEL, STATUS_LABEL, EXECUTOR_LABEL, LABELS_LABEL,
    MY_TASKS_ONLY, FILTER_LABEL)

NAME = 'name'
DESCRIPTION = 'description'
STATUS = 'status'
EXECUTOR = 'executor'
LABELS = 'labels'
ID = 'id'


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [NAME, DESCRIPTION, STATUS, EXECUTOR, LABELS]
        labels = {
            NAME: NAME_LABEL,
            DESCRIPTION: DESCRIPTION_LABEL,
            STATUS: STATUS_LABEL,
            EXECUTOR: EXECUTOR_LABEL,
            LABELS: LABELS_LABEL}


class TaskFilter(django_filters.FilterSet):
    all_statuses = Status.objects.values_list(ID, NAME, named=True).all()
    status = django_filters.filters.ChoiceFilter(
        label=STATUS_LABEL,
        choices=all_statuses,
    )
    all_executors = User.objects.values_list(
        ID,
        Concat('first_name', Value(" "), 'last_name'),
        named=True,
    ).all()
    executor = django_filters.filters.ChoiceFilter(
        label=EXECUTOR_LABEL,
        choices=all_executors,
    )
    all_labels = Label.objects.values_list(ID, NAME, named=True).all()
    labels = django_filters.filters.ChoiceFilter(
        label=FILTER_LABEL,
        choices=all_labels,
    )
    self_task = django_filters.filters.BooleanFilter(
        label=MY_TASKS_ONLY,
        widget=forms.CheckboxInput(),
        method="filter_self",
    )

    def filter_self(self, queryset, name, value):
        if value:
            author = getattr(self.request, "user", None)
            queryset = queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
