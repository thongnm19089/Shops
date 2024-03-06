import uuid

from django.db import models
from . import Product, Variant
from core.models import UploadTo


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True, blank=True)
    file_name = models.CharField(max_length=100, blank=False, null=False)
    path = models.FileField(
        upload_to=UploadTo("shops", "product"),
        max_length=1024,
    )
    size = models.IntegerField(blank=False, null=False)
    position = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
