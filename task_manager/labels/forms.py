from django import forms

from .models import Label
from .translations import NAME_TITLE

NAME = 'name'


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = [NAME]
        labels = {
            NAME: NAME_TITLE,
        }
