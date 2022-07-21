from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
USERNAME = 'username'
PASSWORD1 = 'password1'
PASSWORD2 = 'password2'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            FIRST_NAME,
            LAST_NAME,
            USERNAME,
            PASSWORD1,
            PASSWORD2,
        ]
