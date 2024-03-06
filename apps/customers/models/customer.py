import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.db.models.enums import Choices
from django.utils.translation import gettext_lazy as _
import slugify

from apps.shops.models import Branch
from core.models import UploadTo
# from .customer_group import CustomerGroup
from .career import Career
from core.util import get_generated_code
# from apps.activity_logs.registry import activity_log
# from core.util import get_district_city

from ...users.models.user import User

class Gender(models.TextChoices):
    UNKNOWN = 'UNKNOWN', _('UNKNOWN')
    MALE = 'MALE', _('MALE')
    FEMALE = 'FEMALE', _('FEMALE')

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    ascii_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.UNKNOWN
    )
    branches = models.ManyToManyField(
        Branch,
        blank=True,
        null=True,
        related_name="branches",
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    day_of_birth = models.PositiveSmallIntegerField(blank=True, null=True)
    month_of_birth = models.PositiveSmallIntegerField(blank=True, null=True)
    year_of_birth = models.PositiveSmallIntegerField(blank=True, null=True)
    avatar_url = models.FileField(
        upload_to=UploadTo('shops', 'customer'),
        max_length=1024,
        blank=True,
        null=True
    )
    facebook = models.CharField(max_length=200, blank=True, null=True)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, blank=True, null=True)
    note = models.TextField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "customer"
        constraints = [
            models.UniqueConstraint(fields=['phone'], name='unique_customer_phone'),
            models.UniqueConstraint(fields=['code'], name='unique_customer_code'),
        ]
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_generated_code(Customer, 'C')
        self.ascii_name = slugify.slugify(self.name, separator=' ')
        super(Customer, self).save(*args, **kwargs)

    def get_gender(self):
        GENDER_MAP = {
            "MALE": "Nam",
            "FEMALE": "Nữ",
            "UNKNOWN": ""
        }
        return GENDER_MAP.get(self.gender)

    def get_birth_day(self):
        day = self.day_of_birth
        month = self.month_of_birth
        year = self.year_of_birth
        if day and month and year:
            return f'{day}/{month}/{year}'
        if day and month:
            return f'{day}/{month}'
        if month and year:
            return f'{month}/{year}'
        if year:
            return f'{year}'
        return ""

# activity_log.register(Customer)