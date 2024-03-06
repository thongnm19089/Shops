import uuid

from django.db import models

from apps.users.models.user import User
from .notification_category import NotificationCategory


class NotificationSetting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    category = models.ForeignKey(
        NotificationCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    enabled = models.BooleanField(blank=False, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
