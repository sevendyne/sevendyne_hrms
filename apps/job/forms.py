from django import forms
from django.forms.widgets import TextInput, Select,URLInput, ClearableFileInput
from apps.candidate.models import Candidate
from apps.employee.models import Department
from apps.job.models import CandidateInterview, CandidateJob, Job, JobApplicant
from datetime import date
from django.utils.translation import gettext_lazy as _


class DateInput(forms.DateInput):
    input_type = 'date'
    value = date.today() 


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['creator', 'updator', 'auto_id','a_id','company','is_deleted'] 
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Job Title'}),
            'department': forms.Select(attrs={'class': 'required form-control ', 'placeholder': 'Department'}),
            'job_location': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Job Location'}),
            'no_of_vacancies': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'No of Vacancies'}),
            'experience': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Experience'}),  
            'age': forms.TextInput(attrs={'class': 'required form-control', 'placeholder': 'Age'}),
            'salary_from': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salary From'}),
            'salary_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salary To'}),
            'job_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Job Type'}),
            'job_category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Job Category'}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'start_date': DateInput(attrs={'class': 'form-control datetimepicker', 'placeholder': 'Start Date'}),
            'expired_date': DateInput(attrs={'class': 'form-control datetimepicker', 'placeholder': 'Expired Date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }
        error_messages = {
            'job_title': {
                'required': _("Job Title field is required."),
            },
            'job_type': {
                'required': _("Job Type field is required."),
            },
            'status': {
                'required': _("Status field is required."),
            }
        }
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(JobForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter department by current company
            self.fields['department'].queryset = Department.objects.filter(company=current_company, is_deleted=False)            
      


class CandidateJobForm(forms.ModelForm):
    class Meta:
        model = CandidateJob
        exclude = ['company','candidate','status','is_deleted'] 
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Job Title'}),
            'job_location': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Job Location'}),
            'salary_from': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salary From'}),
            'salary_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salary To'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }
        error_messages = {
            'job_title': {
                'required': _("Job Title field is required."),
            }
        }


class CandidateJobStatusForm(forms.ModelForm):
    class Meta:
        model = CandidateJob
        exclude = ['company','candidate','is_deleted','job_title','job_location','salary_from','salary_to','description'] 
        widgets = {
            'status': forms.Select(attrs={'class': 'required form-control ', 'placeholder': 'Status'})
        }
        error_messages = {
            'status': {
                'required': _("Job Status field is required."),
            }
        }


class CandidateInterviewForm(forms.ModelForm):
    class Meta:
        model = CandidateInterview
        exclude = ['creator', 'updator', 'auto_id','a_id','company','candidate','is_deleted','interview_status'] 
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'additional_information': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Information'})
        }
        error_messages = {
            'date_time': {
                'required': _("Date Time field is required."),
            }
        }


class CandidateInterviewStatusForm(forms.ModelForm):
    class Meta:
        model = CandidateInterview
        fields = ['interview_status'] 
        widgets = {
            'interview_status': forms.Select(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }
        error_messages = {
            'interview_status': {
                'required': _("Interview Status field is required."),
            }
        }


class JobApplicantForm(forms.ModelForm):
    class Meta:
        model = JobApplicant
        fields = ['candidate'] 
        widgets = {
            'candidate': forms.Select(attrs={'class': 'required form-control ', 'placeholder': 'Candidate'})
        }
        error_messages = {
            'candidate': {
                'required': _("Candidate field is required."),
            }
        }
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(JobApplicantForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter candidate by current company
            self.fields['candidate'].queryset = Candidate.objects.filter(company=current_company, is_deleted=False)            
            # Filter job by current company
            self.fields['job'].queryset = Job.objects.filter(company=current_company, is_deleted=False)
           

class JobApplicantStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplicant
        exclude = ['hiring_status'] 
        widgets = {
            'hiring_status': forms.Select(attrs={'class': 'required form-control ', 'placeholder': 'Hiring Status'})
        }
        error_messages = {
            'hiring_status': {
                'required': _("Hiring Status field is required."),
            }
        }
    def __init__(self, *args, **kwargs):
        current_company = kwargs.pop('current_company', None)
        super(JobApplicantStatusForm, self).__init__(*args, **kwargs)        
        if current_company:
            # Filter candidate by current company
            self.fields['candidate'].queryset = Candidate.objects.filter(company=current_company, is_deleted=False)            
            
