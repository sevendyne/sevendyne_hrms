from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from main.models import BaseModel

JOBTYPE_CHOICES = (
    ('Full Time', "Full Time"),
    ('Part Time',"Part Time"),
    ('Contract',"Contract")
)

DOMAIN_CHOICES = (
    ('Full Stack Development', "Full Stack Development"),
    ('Marketing',"Marketing"),
    ('Accounting',"Accounting"),
    ('Design Engineering',"Design Engineering"),
    ('Matlab',"Matlab"),
)

class Candidate(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_("First Name"),max_length=100)
    last_name = models.CharField(_("Last Name"),max_length=100)
    email = models.EmailField(_("Email"),unique=True)
    photo = models.ImageField(_("Photo"),upload_to='candidates/photos/', null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"),max_length=255)
    address = models.TextField(_("Address"),null=True, blank=True)
    education = models.TextField(_("Highest Level Of Education"),null=True, blank=True)
    experience = models.TextField(_("Experience in years"),null=True, blank=True)
    skills = models.TextField(_("Skills")) #formset
    certifications = models.FileField(upload_to='candidates/certificates/', null=True, blank=True) #formset
    projects = models.URLField(_("Portfolio/ Work Samples/ Github Links"),null=True, blank=True) #formset
    additional_information = models.TextField(null=True, blank=True) # formset
    linkedin_profile = models.URLField(_("LinkedIn Profile Link"),null=True, blank=True)
    github_profile = models.URLField(_(" Github Links"),null=True, blank=True)
    resume = models.FileField(upload_to='candidates/resumes/', null=True, blank=True)
    date_applied = models.DateTimeField(auto_now_add=True)
    candidateid = models.CharField(_('Candidate ID'),max_length=255,unique=True,null=True,blank=True)    
    job_type = models.CharField(_("Select Job Type"),max_length=255, choices=JOBTYPE_CHOICES,default='Full Time')
    is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle candidate block and unblock',default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        ordering = ['-date_applied']



# Create your models here.
class Intern(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(_("Email"),unique=True)
    phone = models.CharField(_("Phone Number"),max_length=255)
    intern_linkedin = models.URLField(_("linkedin Profile Link"),null=True,blank=True,max_length = 255)
    intern_git = models.URLField(_("GitHub Profile Link"),null=True,blank=True,max_length = 255)
    resume = models.FileField(_("Upload your resume"),upload_to='resumes/',null=True,blank=True)
    skills = models.CharField(max_length=255,null=True,blank=True)
    domain = models.CharField(_("Select your domain"),max_length=255, choices=DOMAIN_CHOICES,default='Full Stack Development')
    date_added = models.DateTimeField(db_index=True,auto_now_add=True) 
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = ('candidate_intern')
        verbose_name = _('intern')
        verbose_name_plural = _('interns')

    def __str__(self):
        return self.name   
