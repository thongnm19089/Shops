import uuid
import slugify

from django.db import models
from ..models import Product, Brand, Category
from django.db.models import JSONField


class Variant(models.Model):
    # objects = CustomManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=100, unique=True)
    ascii_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField(blank=False, null=False)
    barcode = models.CharField(max_length=20, null=True, blank=True, unique=True)
    sku = models.CharField(max_length=20, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    options = JSONField(blank=True, null=True)
    sellable = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="variants",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="variants",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "variant"
        ordering = ["created_at"]
