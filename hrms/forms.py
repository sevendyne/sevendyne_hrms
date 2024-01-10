from django import forms
from django.utils.translation import gettext_lazy as _
from .models import HrmsClient

class HrmsClientForm(forms.ModelForm):
    class Meta:
        model = HrmsClient
        exclude = ['is_deleted','user'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'required form-control ', 'placeholder': 'example@example.com'}),
            'username': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'User Name'}),
            'password': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Password'}),  # Display password field as a password input
            'employee_profile_url': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Odoo Employee Profile Url'}),
            'leave_application_url': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Odoo Leave Application Url'}),
            'payroll_salary_url': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Odoo Payroll Salary Url'}),            
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
