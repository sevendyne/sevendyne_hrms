from datetime import date
import datetime
from django import forms
from django.forms.widgets import TextInput, Select,URLInput, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from employee.models import AttendanceRegister, Department, Designation, Employee, Leave, LeaveType


class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 


class DepartmentForm(forms.ModelForm):
    
    class Meta:
        model = Department
        exclude = ['creator','updator','auto_id','a_id','company','is_deleted']
        widgets = {            
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Designation name'})            
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
    # class Meta:
    #     model = Designation
    #     exclude = ['creator', 'updator', 'auto_id', 'is_deleted']
    #     widgets = {
    #         'section':Select(attrs={'class':'required form-control'}),
    #     }
    #     error_messages = {
    #         'section': {
    #             'required': _("section field is required."),
    #         }            
    #     }

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


class LeaveForm(forms.ModelForm):
    remaining_days = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    
    class Meta:
        model = Leave
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted','employee','is_approved','status'] 
        widgets = {
            'reason': TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason for leave'}),
            'leave_days': TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),
            'leavetype': Select(attrs={'class': 'required form-control'}),
            'startdate' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
            'enddate' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
            'startdate' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
        }
        error_messages = {
            'reason': {
                'required': _("reason field is required."),
            },
            'leavetype': {
                'required': _("Leave Type field is required."),
            },
            'enddate': {
                'required': _("enddate field is required."),
            },
            'startdate': {
                'required': _("startdate field is required."),
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



class AttendanceRegisterForm(forms.ModelForm):

    ATTENDANCE_CHOICES = (                
        ('True', 'Present'), 
        ('False', 'Absent'),                
        )
    
    employee_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'required  form-control'}))
    employee_pk = forms.CharField(widget=forms.TextInput(attrs={'class': 'required  form-control'}))
    is_attended = forms.CharField(
        max_length=20,
        widget=forms.Select(choices = ATTENDANCE_CHOICES,attrs={'class' : 'form-control '}),
        required=False
    )
    is_fn = forms.CharField(
        max_length=20,
        widget=forms.Select(choices = ATTENDANCE_CHOICES,attrs={'class' : ' '}),
        required=False
    )
    is_an = forms.CharField(
        max_length=20,
        widget=forms.Select(choices = ATTENDANCE_CHOICES,attrs={'class' : ' '}),
        required=False
    )
    class Meta:
        model = AttendanceRegister
        fields = []        
        widgets = {   
                   
        }, 
        error_messages = {
            
        }
       
class AttendanceDateForm(forms.ModelForm): 
    an_fn_CHOICES = (                
        ('FN', 'Forenoon'), 
        ('AN', 'Afternoon'),
        )
    
    an_fn = forms.CharField(
        max_length=20,
        widget=forms.Select(choices = an_fn_CHOICES,attrs={'class' : ' form-control', 'placeholder': 'Select FN/AN'}),
        required=False
    )   
    class Meta:
        model = AttendanceRegister       
        fields = ['date']
        widgets = {       
            'date': DateInput(format = '%Y-%m-%d',attrs={'type': 'date','class' : ' form-control'}),
        }
        error_messages = {
            'date' : {
                'required' : ("date field is required."),
            }
        }
