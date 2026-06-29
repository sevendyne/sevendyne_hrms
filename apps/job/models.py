import datetime
from django.db import models
from apps.main.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = (
    ('Open', "Open"),
    ('Close',"Close")
)

JOBTYPE_CHOICES = (
    ('Full Time', "Full Time"),
    ('Part Time',"Part time"),
    ('Internship', "Internship"),
    ('Contract', "Contract")
)

JOBCATEGORY_CHOICES = (
    ('Full Stack Development', "Full Stack Development"),
    ('Marketing',"Marketing"),
    ('Accounting', "Accounting"),
    ('Design Engineering', "Design Engineering"),
    ('Matlab', "Matlab"),
)

JOB_STATUS_CHOICES = (
    ('No Offer', "No Offer"),
    ('Offer a job', "Offer a job"),
    ('Job Offered',"Job Offered"),
    ('Assign Task',"Assign Task"),
    ('Interested in the Job',"Interested in the Job"),
    ('Interview Scheduled',"Interview Scheduled"),
    ('Interview Done',"Interview Done"),
    ('Cancelled/Rejected',"Cancelled/Rejected")
)

INTERVIEW_CHOICES = (
    ('Interview not done', "Interview not done"),
    ('Sent an offer letter', "Sent an offer letter"),
    ('Better luck next time',"Better luck next time"),
    ('Waiting List',"Waiting List"),
    ('Rejected',"Rejected")
)

JOB_APPLICANT_STATUS_CHOICES = (
    ('Not an applicant', "Not an applicant"),
    ('Applicant', "Applicant"),
    ('Hired',"Hired"),
    ('Assign Task',"Assign Task"),
    ('Interview Scheduled',"Interview Scheduled"),
    ('Interview Done',"Interview Done"),
    ('Cancelled/Rejected',"Cancelled/Rejected")
)
class Job(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    job_title = models.CharField(_('Job Title'),max_length=255)
    department = models.ForeignKey("employee.Department",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False},null=True, blank=True)
    job_location = models.CharField(_('Job Location'),max_length=255,null=True, blank=True)   
    no_of_vacancies = models.CharField(_('Number Of Vacancies'),max_length=100,null=True, blank=True)
    experience = models.CharField(_("Experience"),max_length=255,null=True, blank=True)
    age = models.PositiveIntegerField(_("Age"),null=True, blank=True)
    salary_from = models.PositiveIntegerField(_("Salary From"),null=True, blank=True)
    salary_to = models.PositiveIntegerField(_("Salary To"),null=True, blank=True)
    job_type =  models.CharField(max_length=255, choices=JOBTYPE_CHOICES,null=True, blank=True)
    job_category =  models.CharField(max_length=255, choices=JOBCATEGORY_CHOICES,default='Full Stack Development')
    status =  models.CharField(max_length=255, choices=STATUS_CHOICES)
    start_date = models.DateField(_('Start Date'),help_text='start date',null=True, blank=True)    
    expired_date = models.DateField(_('Expired Date'),help_text='expired date',null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

   
    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
        ordering = ['job_title']

    def __str__(self):
        return self.job_title
    

class CandidateJob(models.Model):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    candidate = models.ForeignKey("candidate.Candidate",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})     
    job_title = models.CharField(_('Job Title'),max_length=255)
    job_location = models.CharField(_('Job Location'),max_length=255,null=True, blank=True)   
    description = models.TextField(null=True, blank=True)
    salary_from = models.PositiveIntegerField(_("Salary From"),null=True, blank=True)
    salary_to = models.PositiveIntegerField(_("Salary To"),null=True, blank=True)
    status =  models.CharField(max_length=255, choices=JOB_STATUS_CHOICES, default="Offer a job")
    # interview_status =  models.CharField(max_length=255, choices=INTERVIEW_CHOICES, default="Interview not done")
    is_deleted = models.BooleanField(default=False)

   
    class Meta:
        verbose_name = _('CandidateJob')
        verbose_name_plural = _('CandidateJobs')
        ordering = ['job_title']

    def __str__(self):
        return self.job_title
    
class CandidateInterview(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    candidate = models.ForeignKey("candidate.Candidate",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})     
    date_time = models.DateTimeField()
    additional_information = models.TextField(null=True, blank=True)
    interview_status =  models.CharField(max_length=255, choices=INTERVIEW_CHOICES)
    is_deleted = models.BooleanField(default=False)

   
    class Meta:
        verbose_name = _('CandidateInterview')
        verbose_name_plural = _('CandidateInterviews')
        ordering = ['date_time']

    def __str__(self):
        return self.date_time
    

class JobApplicant(BaseModel):
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    candidate = models.ForeignKey("candidate.Candidate",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})     
    job = models.ForeignKey("job.Job",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})   
    hiring_status =  models.CharField(max_length=255, choices=JOB_APPLICANT_STATUS_CHOICES, default="Not an Applicant")
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

   
    class Meta:
        verbose_name = _('JobApplicant')
        verbose_name_plural = _('JobApplicants')
        ordering = ['job']

    def __str__(self):
        return self.job
    

