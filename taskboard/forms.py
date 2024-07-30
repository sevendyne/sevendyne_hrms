from datetime import date
from django import forms
from django.forms.widgets import TextInput, Select, FileInput, SelectMultiple, Textarea
from employee.models import Employee
from taskboard.models import COLOUR_CHOICES, Project, TaskBoard
from django.utils.translation import gettext_lazy as _


class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['creator', 'updator', 'auto_id', 'a_id','is_deleted','company'] 
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
            'start_date' : DateInput(attrs={'class' : 'datetimepicker form-control'}),  
            'end_date' : DateInput(attrs={'class' : 'datetimepicker form-control'}) , 
            'priority': Select(attrs={'class': 'required form-control selectpicker'}),
            'project_leader': Select(attrs={'class': 'required form-control'}),
            'team': SelectMultiple(attrs={'class': 'required form-control selectpicker', 'multiple': 'multiple'}),
            'file': FileInput(),   
            'description': Textarea(attrs={'class': 'required form-control ', 'placeholder': 'Description'})
        }
        error_messages = {
            'name': {
                'required': _("Name field is required."),
            }
        }
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        if current_company:
            employees = Employee.objects.filter(company=current_company, is_deleted=False)

            # Customize project_leader field
            self.fields['project_leader'].queryset = employees     
            
            # Adding data-photo-url attribute to project_leader field options
            self.fields['project_leader'].widget.choices = [
                (employee.id, employee.get_full_name) for employee in employees
            ]
            for employee in employees:
                self.fields['project_leader'].widget.attrs.update({
                    f'data-photo-url-{employee.id}': employee.photo.url if employee.photo else ''
                })

            # Customize team field
            self.fields['team'].queryset = employees
            self.fields['team'].widget.choices = [
                (employee.id, employee.get_full_name()) for employee in employees
            ]
            for employee in employees:
                self.fields['team'].widget.attrs.update({
                    f'data-photo-url-{employee.id}': employee.photo.url if employee.photo else ''
                })


class TaskBoardForm(forms.ModelForm):    
    class Meta:
        model = TaskBoard
        exclude = ['creator','updator','auto_id','a_id','company','is_deleted']
        widgets = {            
            'name': TextInput(attrs={'class': 'required form-control', 'placeholder': 'Enter Task Board name'}),
            'project': Select(attrs={'class': 'required form-control'}),
            'color': forms.RadioSelect(choices=COLOUR_CHOICES)
        }
        error_messages = {
            'name' : {
                'required' : _("name field is required."),
            },
            'project' : {
                'required' : _("project field is required."),
            }
        }
        autocomplete = {
            'project': 'on',  # or 'off' if you want to disable autocomplete
        }
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(TaskBoardForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter departments by current company
            self.fields['project'].queryset = Project.objects.filter(company=current_company, is_deleted=False)
        
# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         exclude = ['creator','updator','auto_id','a_id','company','is_deleted'] 
#         widgets = {
#             'name': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Name'}),
#             'priority': Select(attrs={'class': 'form-control selectpicker'}), 
#             'due_date' : DateInput(attrs={'class' : 'datetimepicker form-control'}),
#             'description': TextInput(attrs={'class': 'form-control ', 'placeholder': 'Description'}),
#             'employee': Select(attrs={'class': 'required form-control'}),
#             'project': Select(attrs={'class': 'required form-control'}),
#             'attachment': FileInput()         
#         }
#         error_messages = {                     
#             'name': {
#                 'required': _("Name field is required."),
#             },
#             'employee': {
#                 'required': _("employee field is required."),
#             },
#             'project': {
#                 'required': _("project field is required."),
#             }
#         }


# class TaskcommentForm(forms.ModelForm):
#     class Meta:
#         model = Taskcomment
#         exclude = ['creator', 'updator', 'auto_id','is_deleted'] 
#         widgets = {
#             'company': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Company Name'}),
#             'employee': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Employee Name'}),
#             'task': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Task'}),
#             'comment': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'comment'}),
#             'image': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Image'}),    
#             'file': TextInput(attrs={'class': 'required form-control ', 'placeholder': 'File'})  

#         }
#         error_messages = {
#             'company': {
#                 'required': _("Company field is required."),
#             },
#             'employee': {
#                 'required': _("Employee field is required."),
#             },
#              'task': {
#                 'required': _("Task  field is required."),
#             },
#              'comment': {
#                 'required': _("Comment field is required."),
#             },
#             'image': {
#                 'required': _("Image field is required."),
#             },
#             'file': {
#                 'required': _("File field is required."),
#             }
        

#         }