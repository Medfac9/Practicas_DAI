from django import forms
from django.core.exceptions import ValidationError

class NameForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    tipo = forms.CharField(label='tipo', max_length=100)

class Usuario(forms.Form):
    correo = forms.CharField(label='correo', max_length=100)
    contra = forms.CharField(label='contra', max_length=100)