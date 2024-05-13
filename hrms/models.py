from django.db import models
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
        return f"{self.get_full_name}"
    
    @property
    def get_full_name(self):
        if self.lastname:
            full_name = f"{self.first_name} {self.last_name}"
        else:
            full_name = self.first_name
        return full_name
    
