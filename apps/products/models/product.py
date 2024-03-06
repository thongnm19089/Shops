import uuid
import slugify

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.models import CustomManager
from .category import Category
from .brand import Brand
# from apps.activity_logs.registry import activity_log
from core.models import UploadTo


class Product(models.Model):
    # objects = CustomManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    ascii_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
    )
    status = models.BooleanField(default=True)
    landing_page_position = models.PositiveIntegerField(blank=True, null=True)
    landing_page_active = models.BooleanField(blank=True, null=True, default=False)
    landing_page_show_price = models.BooleanField(default=True)

    class Meta:
        db_table = "product"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_product_name",
            )
        ]

    def save(self, *args, **kwargs):
        self.ascii_name = slugify.slugify(self.name, separator=' ')
        super(Product, self).save(*args, **kwargs)

# activity_log.register(Product)
