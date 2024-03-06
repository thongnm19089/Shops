import uuid

# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from django.db import models

from .notification_category import NotificationCategory
from apps.users.models import User
from apps.customers.models import Customer
# from apps.notifications.constant import *


class NotificationEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_id = models.UUIDField(blank=True, null=True)
    model = models.CharField(max_length=30, blank=True, null=True)
    action = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(
        NotificationCategory,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="notification_events",
    )
    trigger = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="notification_event_trigger",
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True,
    )
    message_data = JSONField(blank=True, null=True)  # for cms message
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification_event"
        ordering = ["created_at"]

    # def save(self, keep_deleted=False, **kwargs):
    #     if self.model and self.model_id:
            # if self.model == APPOINTMENT_MODEL:
            #     appointment = Appointment.objects.all_with_deleted().get(pk=self.model_id)
            #     self.customer_id = appointment.customer_id
            # if self.model == INVOICE_MODEL:
            #     invoice = Invoice.objects.get(pk=self.model_id)
            #     self.customer_id = invoice.customer_id
            # if self.model == RECEIPT_MODEL:
            #     receipt = Receipt.objects.get(pk=self.model_id)
            #     self.customer_id = receipt.customer_id
            # if self.model == CUSTOMER_ITEM_MODEL:
            #     customer_item = CustomerItem.objects.get(pk=self.model_id)
            #     self.customer_id = customer_item.customer_id
        # super(NotificationEvent, self).save(keep_deleted=keep_deleted, **kwargs)
