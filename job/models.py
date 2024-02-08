import datetime
from django.db import models
from main.models import BaseModel
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
    ('Contract', "Contract"),
)

class Job(BaseModel):  
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False}) 
    job_title = models.CharField(_('Job Title'),max_length=125)
    department = models.ForeignKey("employee.Department",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    job_location = models.CharField(_('Job Location'),max_length=125)   
    no_of_vacancies = models.CharField(_('Number Of Vacancies'),max_length=100)
    experience = models.EmailField(_("Experience"),unique=True)
    Age = models.PositiveIntegerField(_("Age"))
    salary_from = models.PositiveIntegerField(_("Salary From"))
    salary_to = models.PositiveIntegerField(_("Salary To"))
    job_type =  models.CharField(max_length=128, choices=JOBTYPE_CHOICES, default='Additions')
    status =  models.CharField(max_length=128, choices=STATUS_CHOICES, default='Additions')
    start_date = models.DateField(_('Start Date'),help_text='start date')    
    expired_date = models.DateField(_('Expired Date'),help_text='expired date')
    description = models.CharField(max_length=254)
    is_deleted = models.BooleanField(default=False)

   
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['firstname']

    def __str__(self):
        return self.get_full_name
