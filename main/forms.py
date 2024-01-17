from datetime import date
from django import forms
from django.forms.widgets import TextInput, Select, Textarea
from django.utils.translation import gettext_lazy as _
from main.models import Company
# from dal import autocomplete

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 

class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        exclude = ['creator','updator','auto_id','user','is_deleted']
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
    # def __init__(self, *args, **kwargs):
    #     super(CompanyForm, self).__init__(*args, **kwargs)
    #     self.fields['country'].widget.attrs['id'] = 'id_country'  # Add this line
    #     self.fields['state'].widget.attrs['id'] = 'id_state'
