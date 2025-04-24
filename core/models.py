from django.contrib.auth.models import User
from django.db import models

from .utils import generate_id


class BaseModel(models.Model):
    id = models.CharField(
        max_length=100, primary_key=True, default=generate_id, editable=False
    )
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
