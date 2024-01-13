from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from main.models import BaseModel

# Refer https://internshala.com/student/resume?detail_source=resume_direct#personal_details 
#check internshala,naukri etc
class Candidate(BaseModel):
    first_name = models.CharField(_("First Name"),max_length=100)
    last_name = models.CharField(_("Last Name"),max_length=100)
    email = models.EmailField(_("Email"),unique=True)
    photo = models.ImageField(_("Photo"),upload_to='photos/', null=True, blank=True)
    phone_number = PhoneNumberField(_("Phone Number"))
    address = models.TextField(_("Address"),null=True, blank=True)
    education = models.TextField(_("Highest Level Of Education"),null=True, blank=True)
    experience = models.TextField(_("Experience in years"),null=True, blank=True)
    skills = models.TextField(_("Skills"),null=True, blank=True)
    certifications = models.FileField(upload_to='certificates/', null=True, blank=True)
    projects = models.URLField(_("Portfolio/ Work Samples/ Github Links"),null=True, blank=True)
    # programming_languages = models.TextField(null=True, blank=True) #formset
    # database_management = models.TextField(null=True, blank=True)
    # version_control = models.TextField(null=True, blank=True)
    additional_information = models.TextField(null=True, blank=True) # formset
    linkedin_profile = models.URLField(_("LinkedIn Profile Link"),null=True, blank=True)
    github_profile = models.URLField(_(" Github Links"),null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    date_applied = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        ordering = ['-date_applied']
