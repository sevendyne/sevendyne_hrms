from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from main.models import BaseModel


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
    certifications = models.TextField(_("Certifications"),null=True, blank=True)
    projects = models.TextField(null=True, blank=True)
    programming_languages = models.TextField(null=True, blank=True)
    database_management = models.TextField(null=True, blank=True)
    version_control = models.TextField(null=True, blank=True)
    additional_information = models.TextField(null=True, blank=True)
    linkedin_profile = models.URLField(null=True, blank=True)
    github_profile = models.URLField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    date_applied = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        ordering = ['-date_applied']
