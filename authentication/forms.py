from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    studio_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'studio_name', 'password1']

