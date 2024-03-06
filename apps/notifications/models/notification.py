import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .notification_event import NotificationEvent
from apps.shops.models.branch import Branch
from apps.shops.models.shop import Shop
from apps.users.models.user import User
from .notification_category import NotificationCategory


class NotificationState(models.TextChoices):
    WAITING = 'WAITING', _('WAITING')
    DELIVERED = 'DELIVERED', _('DELIVERED')
    SEEN = 'SEEN', _('SEEN')


class NotificationType(models.TextChoices):
    ACTION = 'ACTION', _('ACTION')
    NEWS = 'NEWS', _('NEWS')


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    category = models.ForeignKey(
        NotificationCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    event = models.ForeignKey(
        NotificationEvent,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    content = models.TextField(blank=True, null=True)
    state = models.CharField(
        max_length=10,
        choices=NotificationState.choices,
        default=NotificationState.WAITING
    )
    delivery_at = models.DateTimeField(blank=True, null=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    model_id = models.UUIDField(blank=True, null=True)
    model = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        default=NotificationType.ACTION,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
