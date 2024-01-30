from datetime import date
import datetime
from django import forms
from django.forms.widgets import TextInput, Select,URLInput, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from employee.models import Department, Designation, Employee, LeaveType

class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 


class DepartmentForm(forms.ModelForm):
    
    class Meta:
        model = Department
        exclude = ['creator','updator','auto_id','a_id','company','is_deleted']
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
        exclude = ['creator','updator','auto_id','a_id','company','is_deleted']
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
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted','user'] 
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'required form-control ', 'placeholder': 'example@example.com'}),
            'username': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'User Name'}),
            'password': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Password'}),  # Display password field as a password input
            'phone': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter phone number'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'client_company': Select(attrs={'class': 'required form-control', 'placeholder': 'Enter company name'}),
            'department': Select(attrs={'class': 'required form-control'}),
            'designation': Select(attrs={'class': 'required form-control'}),
            'employeeid': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter employee id'}),
            'joindate' : DateInput(attrs={'class' : 'datetimepicker form-control'})
        }
        error_messages = {
            'phone': {
                'required': _("Phone Number field is required."),
            },
            'lastname': {
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


class LeaveTypeForm(forms.ModelForm):
    
    class Meta:
        model = LeaveType
        exclude = ['creator','updator','auto_id','a_id','company','is_deleted','is_active']
        widgets = {            
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter leave type name'}),
            'days': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter number of days'})
        }
        error_messages = {
            'name' : {
                'required' : _("name field is required."),
            },
            'days' : {
                'required' : _("days field is required."),
            }
        }


# class LeaveCreationForm(forms.ModelForm):
# 	reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
# 	class Meta:
# 		model = Leave
# 		exclude = ['user','defaultdays','hrcomments','status','is_approved','updated','created']



# 	def clean_enddate(self):
# 		enddate = self.cleaned_data['enddate']
# 		startdate = self.cleaned_data['startdate']
# 		today_date = datetime.date.today()

# 		if (startdate or enddate) < today_date:# both dates must not be in the past
# 			raise forms.ValidationError("Selected dates are incorrect,please select again")

# 		elif startdate >= enddate:# TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
# 			raise forms.ValidationError("Selected dates are wrong")

# 		return enddate

