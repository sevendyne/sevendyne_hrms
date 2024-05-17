from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"{self.username}"
    
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
        message = f"Dear {self.first_name} {self.last_name},\n\nYour account has been enabled.\n\nUsername: {self.username}\nPassword: {self.password}\n\nBest regards,\nHRMS Team"
        recipient_list = [self.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

