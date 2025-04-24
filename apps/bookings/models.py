from django.db import models
from core.models import BaseModel
from storages.backends.s3boto3 import S3Boto3Storage
from core.utils import generate_id
from django.contrib.auth.models import User

# Create your models here.

BOOKING_STATUS = (
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
)


class TicketFileS3Storage(S3Boto3Storage):
    location = "tickets"

def get_tickets_r2_file_path(instance: "Booking", filename: str):
    return f"{generate_id()}.{filename.split(".")[-1]}"


class Booking(BaseModel):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    from_city = models.CharField(max_length=255)
    to_city = models.CharField(max_length=255)
    departure_date = models.DateField()
    passenger_id = models.CharField(max_length=255)
    passenger_name = models.CharField(max_length=255)
    passenger_email = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    price = models.IntegerField(null=True)
    status = models.CharField(max_length=100, choices=BOOKING_STATUS, default="pending")
    ticket = models.FileField(
        max_length=100, storage=TicketFileS3Storage(), upload_to=get_tickets_r2_file_path, null=True
    )

    
