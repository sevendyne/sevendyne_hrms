from django.db import models
from main.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Client(BaseModel):   
    company = models.ForeignKey("main.Company",on_delete=models.CASCADE,limit_choices_to={'is_deleted': False})
    firstname = models.CharField(_('Contact Person Firstname'),max_length=125)
    lastname = models.CharField(_('Contact Person Lastname'),max_length=125,null=False,blank=False)
    email = models.EmailField(_("Email"),unique=True)
    phone = models.CharField(_("Phone Number"),max_length=255)
    address = models.TextField(_("Address"),null=True, blank=True)
    company_name = models.CharField(_('Client Company Name'),max_length=255) #client company foreign key
    clientid = models.CharField(_('Client ID'),max_length=255,null=True,blank=True)
    photo = models.ImageField(_("Photo"), upload_to='client_photos/', null=True, blank=True)
    is_deleted = models.BooleanField(_('Is This Client Deleted ?'),help_text='button to toggle employee deleted and undelete',default=False)
   
    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['company_name']
        unique_together = ('company', 'clientid')

    def __str__(self):
        return  self.company_name 

    @property
    def get_full_name(self):
        if self.lastname:
            full_name = f"{self.firstname} {self.lastname}"
        else:
            full_name = self.firstname
        return full_name