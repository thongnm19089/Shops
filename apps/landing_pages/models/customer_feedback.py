import uuid

from django.db import models

from core.models import UploadTo


class CustomerFeedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(null=False, blank=False, max_length=100)
    customer_image = models.FileField(
        upload_to=UploadTo("shops", "customer_feedback"),
        max_length=1024,
        blank=True,
        null=True,
    )
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "landing_page_feedback"
        ordering = ["created_at"]
