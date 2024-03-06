import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False, null=False)
    color = models.CharField(max_length=20, blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    landing_page_position = models.PositiveIntegerField(blank=True, null=True)
    landing_page_active = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        db_table = "category"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_category_name'
            ),
        ]
