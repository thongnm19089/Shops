import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import UploadTo


class ImageType(models.TextChoices):
    BANNER = "BANNER", _("BANNER")
    WORKSPACE = "WORKSPACE", _("WORKSPACE")


class LandingPageImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.FileField(
        upload_to=UploadTo("shops", "images"),
        max_length=1024,
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=50, null=False, blank=False, choices=ImageType.choices
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "landing_page_image"
        ordering = ["created_at"]
