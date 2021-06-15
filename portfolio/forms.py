from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Photographer

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

class PhotographerForm(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = (
            'first_name',
            'last_name',
            'display_name',
            'show',
        )
        widgets = {
            'show': forms.CheckboxInput(attrs={
                'class': 'tgl-flat'
            })
        }
