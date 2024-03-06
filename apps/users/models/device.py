import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class DeviceOS(models.TextChoices):
    IOS = "IOS", _("IOS")
    ANDROID = "ANDROID", _("ANDROID")
    WEB = "WEB", _("WEB")


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    os = models.CharField(max_length=20, null=True, blank=True, choices=DeviceOS.choices)
    token = models.TextField()
    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='devices'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "device"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["token"],
                name="unique_device_token",
            ),
        ]
