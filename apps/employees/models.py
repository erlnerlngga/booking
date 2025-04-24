from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel

# Create your models here.

ROLE_CHOICE = (
    ("user", "User"),
    ("admin", "Admin"),
)


class EmployeeSetting(BaseModel):
    actor = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=ROLE_CHOICE, default="user")


class Employee(BaseModel):
    actor = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
