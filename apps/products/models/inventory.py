import uuid

from django.db import models

from apps.shops.models import Branch
from .product import Product
from core.models import CustomManager
# from apps.activity_logs.registry import activity_log

class Inventory(models.Model):
    objects = CustomManager()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=False, null=False,
    )
    quantity = models.IntegerField()
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="inventories",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory"
        ordering = ["created_at"]

# activity_log.register(Inventory)
