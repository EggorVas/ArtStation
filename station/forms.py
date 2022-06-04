from django import forms
from .models import Art
from django.contrib.auth.models import User


class ArtForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = ('name', 'author', 'image', 'description', 'style', 'genre', 'technique')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
