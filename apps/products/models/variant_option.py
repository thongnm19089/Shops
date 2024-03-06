import uuid
import slugify
from django.contrib.postgres.fields import ArrayField

from django.db import models
from ..models import Product, Variant


class VariantOption(models.Model):
    # objects = CustomManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    values = ArrayField(
        models.CharField(max_length=10),
        null=True, blank=True, default=None
    )
    position = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        db_table = "variant_option"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "product"],
                name="unique_variant_option_name_product",
            )
        ]
