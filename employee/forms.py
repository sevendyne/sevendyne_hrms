from datetime import date
from django import forms
from django.forms.widgets import TextInput, Select,URLInput, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from employee.models import Department, Designation

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 


class DepartmentForm(forms.ModelForm):
    
    class Meta:
        model = Department
        exclude = ['creator','updator','auto_id','is_deleted']
        widgets = {            
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Designation name'}),
            
        }
        error_messages = {
            'name' : {
                'required' : _("name field is required."),
            }
        }


class DesignationForm(forms.ModelForm):
    
    class Meta:
        model = Designation
        exclude = ['creator','updator','auto_id','is_deleted']
        widgets = {            
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Designation name'}),
            'department': Select(attrs={'class': 'required form-control'})
        }
        error_messages = {
            'name' : {
                'required' : _("first_name field is required."),
            },
            'department' : {
                'required' : _("Department field is required."),
            }
        }
        autocomplete = {
            'department': 'on',  # or 'off' if you want to disable autocomplete
        }

# class DesignationFormset(forms.ModelForm):    
#     class Meta:
#         model = Designation
#         exclude = ['creator', 'updator', 'auto_id', 'is_deleted','department']
#         widgets = {
#             'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Designation name'})
#         }
#         error_messages = {
#             'name': {
#                 'required': _("Name field is required."),
#             }
#         }

# class DesignationForm(forms.ModelForm):    
#     class Meta:
#         model = Designation
#         exclude = ['creator', 'updator', 'auto_id', 'is_deleted']
#         widgets = {
#             'section':Select(attrs={'class':'required form-control'}),
#         }
#         error_messages = {
#             'section': {
#                 'required': _("section field is required."),
#             }            
#         }

# class DesignationEditForm(forms.ModelForm):    
#     class Meta:
#         model = Designation
#         exclude = ['creator', 'updator', 'auto_id','is_deleted']
#         widgets = {
#             'department':Select(attrs={'class':'requird form-control'}),
#             'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Name'}),
#         }
#         error_messages = {
#             'department': {
#                 'required': _("department field is required."),
#             },    
#             'name': {
#                 'required': _("name field is required."),
#             }        
#         }