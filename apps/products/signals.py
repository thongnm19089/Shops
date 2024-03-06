import datetime
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from apps.notifications.handlers.constants import PRODUCT_MINIMUM_INVENTORY_ACTION
from .models.product import Product
from .models.inventory import Inventory
from apps.shops.models import Branch
# from apps.marketings.tasks import process_service_campaigns
from apps.notifications.tasks import process_notification


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def on_created_product(sender, instance, created, **kwargs):
    # if instance.type != 'PRODUCT':
    #     return

    if created:
        # this is creating case of Product
        for branch in Branch.objects.all():
            inventory = Inventory(
                product=instance,
                quantity=0,
                branch=branch,
            )
            inventory.save()


# @receiver(post_save, sender=Inventory)
# def on_upsert_inventory(sender, instance, created, **kwargs):
#     product = instance.product
#     if product.minimum_inventory and instance.quantity <= product.minimum_inventory:
#         process_notification.apply_async(args=(PRODUCT_MINIMUM_INVENTORY_ACTION, instance.id, None))
