from django import forms
from django.forms.widgets import TextInput, Select,URLInput, ClearableFileInput
from payroll.models import PayrollItem, Salary, SalarySetting
from datetime import date
from django.utils.translation import gettext_lazy as _

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 



class SalarySettingForm(forms.ModelForm):
    class Meta:
        model = SalarySetting
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted'] 
        widgets = {
            'da': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Percentage Allowance For DA'}),
            'hra': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Percentage Allowance For HRA'}),
            'pf_emp': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Percentage Allowance For PF Employee'}),
            'pf_org': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Percentage Allowance For PF Organisation'}),
            'esi_emp': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Percentage Allowance For ESI Employee'}),  # Display password field as a password input
            'esi_org': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Percentage Allowance For ESI Organisation'}),
            'tds': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Percentage Allowance For TDS'})
            
        }
        error_messages = {
           
        }


class PayrollItemForm(forms.ModelForm):
    class Meta:
        model = PayrollItem
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'category': Select(attrs={'class': 'required form-control selectpicker'})           
        }
        error_messages = {
            'name': {
                'required': _("Name field is required."),
            },
            'category': {
                'required': _("Category field is required."),
            }
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted'] 
        widgets = {
            'net_salary': forms.TextInput(attrs={'class': 'required form-control '}),
            'employee': Select(attrs={'class': 'required form-control selectpicker'}),
            'date': DateInput(attrs={'class' : 'datetimepicker form-control'})       
        }
        error_messages = {
            'net_salary': {
                'required': _("Net Salary field is required."),
            },
            'employee': {
                'required': _("Employee field is required.")
            },
            'date': {
                'required': _("date field is required."),
            }
        }


# class GeneratePayslipForm(forms.ModelForm):
#     date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     class Meta:
#         model = PaySlip
#         fields = ['date'] 
#         widgets = {       
#             'date': DateInput(format = '%Y-%m-%d',attrs={'type': 'date','class' : ' form-control'}),
#         }
#         error_messages = {
#             'date' : {
#                 'required' : ("date field is required."),
#             }
#         }
