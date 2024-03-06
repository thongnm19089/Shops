import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.shops.models import Branch

from .models import (
    Shift,
    Role,
    User,
    RoleName,
)
from apps.notifications.models import NotificationSetting, NotificationCategory

logger = logging.getLogger(__name__)


def assign_owner_role(user):
    owner_role = Role.objects.filter(name='Owner').first()
    user.role = owner_role
    user.save()
    logger.info(f'set owner role for user {user}')


def init_user_notification_settings(user):
    categories = NotificationCategory.objects.all()
    settings = []
    for category in categories:
        setting = NotificationSetting()
        setting.name = category.name
        setting.user = user
        setting.category_id = str(category.id)
        settings.append(setting)
    NotificationSetting.objects.bulk_create(settings)
    

def set_default_data(user):
    if not user.branch:
        default_branch = Branch.objects.filter(root_branch=True).first()
        user.branch = default_branch
    if not user.shift:
        default_shift = Shift.objects.filter(name="Mặc định").first()
        user.shift = default_shift
    user.save()
    logger.info(f'set default branch and shift for user {user}')


@receiver(post_save, sender=User)
def on_created_user(sender, instance, created, **kwargs):
    if created:
        # if this is first user of tenant, it's the owner
        if instance == User.objects.order_by('created_at').first():
            assign_owner_role(instance)
        set_default_data(instance)
        # if instance.role.name != RoleName.CUSTOMER.value:
        init_user_notification_settings(instance)
            # create_user_time_keeping(instance)
