import uuid
import slugify

from django.db import models
from ..models import Product, Variant


class VariantPrice(models.Model):
    # objects = CustomManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    value = models.PositiveIntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = "variant_price"
