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
    is_enabled = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"
