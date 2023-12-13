from django.contrib.auth.forms import UserCreationForm

from BD.models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User