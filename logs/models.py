from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

from django.db import models

class OperationLog(models.Model):
    OPERATION_CHOICES = (
         ('Create', 'Create'),
         ('Update', 'Update'),
         ('Delete', 'Delete'),
    )

    user_id = models.IntegerField(default=0)  # Valor predeterminado para user_id
    user_username = models.CharField(max_length=150, default="")  # Valor predeterminado para user_username
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.timestamp} - {self.operation} by {self.user_username}"


class SessionLog(models.Model):
    user_id = models.IntegerField(default=0) 
    user_username = models.CharField(max_length=150, default="")  
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user_id}, Username: {self.user_username}, Login Time: {self.login_time}, Logout Time: {self.logout_time}"
