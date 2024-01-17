from datetime import date
from django import forms
from django.forms.widgets import TextInput, URLInput, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from candidate.models import Candidate

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 

class CandidateForm(forms.ModelForm):
    
    class Meta:
        model = Candidate
        exclude = ['creator','updator','auto_id','user','date_applied','is_deleted']
        widgets = {            
            'first_name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Candidate first name'}),
            'last_name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Candidate first name'}),
            'email': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter email id'}),
            'photo': ClearableFileInput(attrs={'class': 'required form-control'}),
            'phone_number': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter phone number'}),
            'address': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter address'}),
            'education': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter highest level of education'}),
            'experience': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter experience in years'}),
            'skills': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter skills'}),
            'certifications': ClearableFileInput(attrs={'class': 'required form-control'}),
            'projects': URLInput(attrs={'class': 'required form-control', 'placeholder': 'Enter portfolio/GitHub links'}),
            'additional_information': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter additional information'}),
            'linkedin_profile': URLInput(attrs={'class': 'required form-control', 'placeholder': 'Enter LinkedIn profile link'}),
            'github_profile': URLInput(attrs={'class': 'required form-control', 'placeholder': 'Enter GitHub profile link'}),
            'resume': ClearableFileInput(attrs={'class': 'required form-control'})
        }
        error_messages = {
            'first_name' : {
                'required' : _("first_name field is required."),
            },
            'last_name' : {
                'required' : _("last_name field is required."),
            },
            'phone' : {
                'required' : _("Phone field is required."),
            },
            'email' : {
                'required' : _("email field is required."),
            },
            'skills' : {
                'required' : _("Skills field is required."),
            }
        }

