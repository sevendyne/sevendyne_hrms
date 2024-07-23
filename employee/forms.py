from datetime import date
import datetime
from django import forms
from django.forms.widgets import TextInput, Select,URLInput, FileInput
from django.utils.translation import gettext_lazy as _
from client.models import Client
from employee.models import AdminHoliday, AttendanceRegister, Department, Designation, Employee, Holiday, Leave, LeaveType
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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
                'required' : _("name field is required."),
            },
            'department' : {
                'required' : _("Department field is required."),
            }
        }
        autocomplete = {
            'department': 'on',  # or 'off' if you want to disable autocomplete
        }
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(DesignationForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter departments by current company
            self.fields['department'].queryset = Department.objects.filter(company=current_company, is_deleted=False)
            
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted','user'] 
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Last Name'}),
            'gender': Select(attrs={'class': 'required form-control'}),
            'email': forms.EmailInput(attrs={'class': 'required form-control ', 'placeholder': 'example@example.com'}),
            'username': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'User Name'}),
            'password': forms.PasswordInput(attrs={'class': 'required form-control ', 'placeholder': 'Password'}),  # Display password field as a password input
            'phone': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter phone number'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            # 'client_company': Select(attrs={'class': 'required form-control', 'placeholder': 'Enter company name'}),
            'department': Select(attrs={'class': 'required form-control'}),
            'designation': Select(attrs={'class': 'required form-control'}),
            'employeeid': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter employee id'}),
            'joindate' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
            'photo': FileInput()
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
    
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(EmployeeForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter departments by current company
            self.fields['department'].queryset = Department.objects.filter(company=current_company, is_deleted=False)            
            # Filter designations by current company
            self.fields['designation'].queryset = Designation.objects.filter(company=current_company, is_deleted=False)

            
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['password', 'photo']
        widgets = {            
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': 'Password'}), 
        }    
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False
        self.fields['password'].required = False


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
            'reason': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Reason for leave'}),
            'leave_days': TextInput(attrs={'readonly': 'readonly','class': 'form-control'}),
            'leavetype': Select(attrs={'class': 'required form-control'}),
            'startdate' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
            'enddate' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
            'startdate' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
            'photo': forms.FileInput()
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
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(LeaveForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter LeaveType by current company
            self.fields['leavetype'].queryset = LeaveType.objects.filter(company=current_company, is_deleted=False)            
            

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
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(AttendanceRegisterForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter employee by current company
            self.fields['employee'].queryset = Employee.objects.filter(company=current_company, is_deleted=False)            

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
        

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'date' : DateInput(attrs={'class' : 'datetimepicker form-control'})         
        }
        error_messages = {
            'name': {
                'required': _("Name field is required."),
            },
            'date': {
                'required': _("Date field is required."),
            }
        }


class AdminHolidayForm(forms.ModelForm):
    class Meta:
        model = AdminHoliday
        exclude = ['is_hide','is_deleted'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'date' : DateInput(attrs={'class' : 'datetimepicker form-control'})         
        }
        error_messages = {
            'name': {
                'required': _("Name field is required."),
            },
            'date': {
                'required': _("Date field is required."),
            }
        }
