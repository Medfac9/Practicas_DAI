from django import forms
from django.core.exceptions import ValidationError

class NameForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    tipo = forms.CharField(label='tipo', max_length=100)