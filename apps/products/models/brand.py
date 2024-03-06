import uuid

from django.db import models
from django.db.models import Q


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "brand"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_brand_name'
            ),
        ]
