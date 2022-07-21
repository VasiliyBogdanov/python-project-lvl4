from django import forms

from .models import Status
from .translations import NAME_TITLE

NAME = 'name'


class StatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = [NAME]
        labels = {
            NAME: NAME_TITLE,
        }
