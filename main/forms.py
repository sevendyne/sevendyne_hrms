from datetime import date
from django import forms
from django.forms.widgets import TextInput, Select, Textarea, FileInput
from django.utils.translation import gettext_lazy as _
from main.models import Company, Portfolio
# from dal import autocomplete

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 

class CompanyForm(forms.ModelForm):    
    class Meta:
        model = Company
        exclude = ['creator','updator','auto_id','is_deleted']
        widgets = {
            
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your company name'}),
            'contact_person': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter name of the contact person'}),
            'address': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your address'}),
            'country': Select(attrs={'class': 'required form-control'}),
            'state': Select(attrs={'class': 'required form-control'}), 
            'city': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your city name'}),
            'postal_code': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your postal code'}),
            'email': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your email id'}),
            'phone': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your phone number'}),
            'mobile': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your mobile number'}),
            'fax': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your fax'}),
            'website': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter your website url'}),
            'logo': FileInput()
        }
        error_messages = {
            'name' : {
                'required' : _("Name field is required."),
            },
            'email' : {
                'required' : _("Email field is required."),
            },
            'phone' : {
                'required' : _("Phone field is required."),
            },
            'address' : {
                'required' : _("Address field is required."),
            },
            'state' : {
                'required' : _("State field is required."),
            },
            'country' : {
                'required' : _("Country field is required."),
            }
        }

class PortfolioForm(forms.ModelForm):    
    class Meta:
        model = Portfolio
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter title'}),
            'description': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Description'}),
            'image': FileInput()
        }
        error_messages = {
            'title' : {
                'required' : _("title field is required."),
            },
            'description' : {
                'required' : _("description field is required."),
            }
        }