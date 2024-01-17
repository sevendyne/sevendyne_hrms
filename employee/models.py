import datetime
from django.db import models
from main.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Department(BaseModel):
    name = models.CharField(_("Department Name"),max_length=125)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Designation(BaseModel):
    name = models.CharField(_("Designation Name"),max_length=255)#formset
    department = models.ForeignKey("employee.Department",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')
        ordering = ['name']

    def __str__(self):
        return self.name


# class Employee(BaseModel):    
        
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     firstname = models.CharField(_('Firstname'),max_length=125,null=False,blank=False)
#     lastname = models.CharField(_('Lastname'),max_length=125,null=False,blank=False)
#     username = models.CharField(max_length=254)    
#     password = models.CharField(max_length=100)
#     email = models.EmailField(_("Email"),unique=True)
#     phone_number = PhoneNumberField(_("Phone Number"))
#     address = models.TextField(_("Address"),null=True, blank=True)
#     department =  models.ForeignKey(Department,verbose_name =_('Department'),on_delete=models.SET_NULL,null=True,default=None)
#     designation =  models.ForeignKey(Designation,verbose_name =_('Designation'),on_delete=models.SET_NULL,null=True,default=None)
#     startdate = models.DateField(_('Employement Date'),help_text='date of employement',blank=False,null=True)    
#     employeeid = models.CharField(_('Employee ID'),max_length=10,null=True,blank=True)

#     # app related
#     is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle employee block and unblock',default=False)
#     is_deleted = models.BooleanField(_('Is Deleted'),help_text='button to toggle employee deleted and undelete',default=False)

   
#     class Meta:
#         verbose_name = _('Employee')
#         verbose_name_plural = _('Employees')
#         ordering = ['firstname']

#     def __str__(self):
#         return self.firstname    

