from django import forms
from .models import Task
from .translations import (
    NAME_LABEL, DESCRIPTION_LABEL, STATUS_LABEL, EXECUTOR_LABEL)

NAME = 'name'
DESCRIPTION = 'description'
STATUS = 'status'
EXECUTOR = 'executor'


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [NAME, DESCRIPTION, STATUS, EXECUTOR]
        labels = {
            NAME: NAME_LABEL,
            DESCRIPTION: DESCRIPTION_LABEL,
            STATUS: STATUS_LABEL,
            EXECUTOR: EXECUTOR_LABEL,
        }
