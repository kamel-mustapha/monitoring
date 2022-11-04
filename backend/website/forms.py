from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext
from django.utils.translation import gettext as _

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class MaximumLengthValidator:
    def __init__(self, max_length=30):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _("Your password must not exceed 30 characters"),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return _("Your password must not exceed 30 characters")