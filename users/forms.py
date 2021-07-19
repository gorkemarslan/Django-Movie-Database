from django import forms
from django.forms.widgets import NumberInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'date_of_birth', 'gender', 'country')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'gender', 'country')


class CustomAuthenticationForm(AuthenticationForm):
    pass
