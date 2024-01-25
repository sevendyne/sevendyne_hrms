from datetime import date
from django import forms
from django.forms.widgets import TextInput, URLInput, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from client.models import Client

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        exclude = ['creator','updator','auto_id','a_id','company','is_deleted']
        widgets = {            
            'firstname': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Client first name'}),
            'lastname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Client first name'}),
            'email': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter email id'}),
            'phone': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter phone number'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'company_name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter company name'}),
            'clientid': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter client id'})
        }
        error_messages = {
            'firstname' : {
                'required' : _("firstname field is required."),
            },
            'phone' : {
                'required' : _("Phone field is required."),
            },
            'email' : {
                'required' : _("email field is required."),
            },
            'company_name' : {
                'required' : _("Company Name field is required."),
            }
        }

