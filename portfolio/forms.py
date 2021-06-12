from django import forms

from .models import Photographer

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
