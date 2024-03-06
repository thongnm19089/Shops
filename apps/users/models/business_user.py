import uuid
from django.db import models
from .user import User
from core.models import UploadTo


class BusinessUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    salary = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    day_of_birth = models.PositiveSmallIntegerField(blank=True, null=True)
    month_of_birth = models.PositiveSmallIntegerField(blank=True, null=True)
    year_of_birth = models.PositiveSmallIntegerField(blank=True, null=True)

    avatar_url = models.FileField(
        upload_to=UploadTo("shops", "user"),
        max_length=1024,
        blank=True,
        null=True,
    )
    color = models.CharField(max_length=15, blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )