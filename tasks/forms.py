from django import forms
from .models import Task
from .translations import (
    NAME_LABEL, DESCRIPTION_LABEL, STATUS_LABEL, EXECUTOR_LABEL, LABELS_LABEL)

NAME = 'name'
DESCRIPTION = 'description'
STATUS = 'status'
EXECUTOR = 'executor'
LABELS = 'labels'


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
