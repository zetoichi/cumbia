from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Photographer


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class PhotographerForm(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = (
            "first_name",
            "last_name",
            "display_name",
            "country",
            "show",
        )
        widgets = {
            "show": forms.CheckboxInput(attrs={"class": "tgl-flat"}),
            "country": forms.Select(
                attrs={
                    "style": "background: none;width: 86%;border: none;border-bottom: 2px solid #999;padding-top: 9px;text-align: center;font-family: termina, sans-serif;"
                }
            ),
        }
