from django import forms
from django.utils.translation import gettext_lazy as _
from .models import HrmsClient


class HrmsClientForm(forms.ModelForm):
    class Meta:
        model = HrmsClient
        exclude = ['is_deleted','is_enabled','user'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'required form-control ', 'placeholder': 'example@example.com'}),
            'username': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'User Name'}),
            'password': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Password'}) 
        }
        error_messages = {
            'first_name': {
                'required': _("First Name field is required."),
            },
            'last_name': {
                'required': _("Last Name field is required."),
            },
            'email': {
                'required': _("Email field is required."),
            },
            'username': {
                'required': _("username field is required."),
            },
            'password': {
                'required': _("password field is required."),
            }
        }

class HrmsClientEditForm(forms.ModelForm):
    class Meta:
        model = HrmsClient
        exclude = ['is_deleted','user'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'required form-control ', 'placeholder': 'example@example.com'}),
            'username': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'User Name'}),
            'password': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Password'}) 
        }
        error_messages = {
            'first_name': {
                'required': _("First Name field is required."),
            },
            'last_name': {
                'required': _("Last Name field is required."),
            },
            'email': {
                'required': _("Email field is required."),
            },
            'username': {
                'required': _("username field is required."),
            },
            'password': {
                'required': _("password field is required."),
            }
        }
