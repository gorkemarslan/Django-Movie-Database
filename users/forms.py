from django import forms
from django.forms.widgets import NumberInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
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


class CustomUserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ('date_of_birth', 'gender', 'country')


class CustomAuthenticationForm(AuthenticationForm):
    pass


class CustomPasswordChangeForm(PasswordChangeForm):

    # Remove help text from new_password1 field
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    # Add all HTML sections of password fields to form-control class
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
