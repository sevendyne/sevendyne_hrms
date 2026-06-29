from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class HrmsClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=254)    
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_attendance_enabled = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Hrms Client')
        verbose_name_plural = _('Hrms Clients')
        ordering = ['first_name']

    def __str__(self):
        return f"{self.username}"
    
    @property
    def get_full_name(self):
        if self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
        else:
            full_name = self.first_name
        return full_name
    
    def save(self, *args, **kwargs):
        # Check if the instance is being enabled for the first time
        if self.pk is not None:
            # Check the current value in the database
            old_instance = HrmsClient.objects.get(pk=self.pk)
            if old_instance.is_enabled == False and self.is_enabled == True:
                # Send email
                self.send_credentials_email()
        elif self.is_enabled:
            # If the instance is new and is_enabled is True
            self.send_credentials_email()

        super(HrmsClient, self).save(*args, **kwargs)

    def send_credentials_email(self):
        subject = 'Your Sevendyne HRMS Account Credentials'
        html_message = render_to_string('sevendyne_admin/hrms_clients/email_hrms_credentials.html', {'username': self.username,'password':self.password,'first_name':self.first_name})
        plain_message = strip_tags(html_message)  # Strip HTML tags for plain text email
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = self.email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)                   
    
    