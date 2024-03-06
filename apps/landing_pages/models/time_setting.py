import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class LandingPageTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    day_of_week = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "landing_page_time_setting"
        ordering = ["created_at"]
