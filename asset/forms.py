from datetime import date
from django import forms
from django.forms.widgets import TextInput, URLInput, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from asset.models import Asset
from candidate.models import Candidate, Intern

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 

class AssetForm(forms.ModelForm):
    
    class Meta:
        model = Asset
        exclude = ['creator','updator','auto_id','a_id','company','is_deleted']
        widgets = {            
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Asset name'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Asset Description'}),
            'purchase_date': DateInput(attrs={'class' : 'required datetimepicker form-control'}),       
            'bill': ClearableFileInput(attrs={'class': 'form-control'}),
            'useful_life_years': TextInput(attrs={'class': 'required form-control', 'placeholder': '[After how many years will this asset expire?]'}),
            'salvage_value': TextInput(attrs={'class': 'required form-control', 'placeholder': '[How much amount will get after expiry date ? ]'}),
            'purchase_price': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter purchase price'}),   
            'photo': ClearableFileInput(attrs={'class': 'required form-control'})         
        }
        error_messages = {
            'name' : {
                'required' : _("Name field is required."),
            },
            'purchase_date' : {
                'required' : _("Purchase Date field is required."),
            },
            'useful_life_years' : {
                'required' : _("Useful Life Years field is required."),
            },
            'salvage_value' : {
                'required' : _("Salvage Value field is required."),
            },
            'purchase_price' : {
                'required' : _("Purchase Price field is required."),
            }
        }
