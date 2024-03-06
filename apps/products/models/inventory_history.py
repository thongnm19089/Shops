import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


from apps.shops.models import Branch
from apps.users.models import User
# from apps.checkouts.models import Invoice
from .product import Product


class Reason(models.TextChoices):
    E_USED = "E_USED", _("E_USED")
    E_DAMAGED = "E_DAMAGED", _("E_DAMAGED")
    E_OUTDATED = "E_OUTDATED", _("E_OUTDATED")
    E_LOSS = "E_LOSS", _("E_LOSS")
    I_NEW = "I_NEW", _("I_NEW")
    I_RETURN = "I_RETURN", _("I_RETURN")
    I_TRANSFER = "I_TRANSFER", _("I_TRANSFER")
    OTHER = "OTHER", _("OTHER")
    ADJUST = "ADJUST", _("ADJUST")


class InventoryHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name="inventory_history",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name="inventory_history",
    )

    is_exported = models.BooleanField(blank=False, null=False)
    reason = models.CharField(
        max_length=30, blank=False, null=False, choices=Reason.choices,
    )
    current_total = models.IntegerField(blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=False, null=False)

    # invoice = models.ForeignKey(
    #     Invoice, on_delete=models.DO_NOTHING, blank=True, null=True,
    # )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=False, null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_history"
        ordering = ["-created_at"]
