from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from restaurant.forms import FormStyleMixin
from users.models import User


class UserRegisterForm(FormStyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "fullname", "phone")


class UserProfileForm(FormStyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "fullname", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
