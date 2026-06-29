from django import forms
from django.forms.widgets import TextInput


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your password'})
    )

