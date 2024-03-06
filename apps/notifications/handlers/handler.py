from django.db.models import Q

from apps.notifications.models import NotificationCategory
from apps.users.models import User, RoleName
from core.notification.utils import (
    create_notification_event_model,
    create_notification_model,
)


class Handler:
    model_class = None
    category_name = None

    def __init__(self, model_object_id, trigger_id, action):
        self.model_object = self.model_class.objects.get(pk=model_object_id)
        self.trigger_id = trigger_id
        self.action = action
        self.category = self._get_category()
        self.event = create_notification_event_model(
            self.model_class.__name__,
            model_object_id,
            action,
            self.category.id,
            trigger_id,
        )
        self.notifications = []

    def _get_category(self):
        return NotificationCategory.objects.get(name=self.category_name)


    def create_notifications(self):
        raise NotImplementedError("Not implemented")

    # def _get_managers_of_branch(self, branch):
    #     return list(
    #         User.objects.filter(
    #             Q(tenant=self.model_object.tenant)
    #             & (
    #                 Q(
    #                     role__name__in=[
    #                         RoleName.OWNER.value,
    #                         RoleName.CHAIN_MANAGER.value,
    #                     ]
    #                 )
    #                 | (
    #                     Q(role__name=RoleName.MANAGER.value)
    #                     & Q(branch=branch)
    #                 )
    #                 | (
    #                     Q(role__name=RoleName.MANAGER.value)
    #                     & Q(
    #                         role__permission_group__in=PermissionGroup.objects.filter(
    #                             name="All Branch"
    #                         )
    #                     )
    #                 )
    #             )
    #         )
    #         .exclude(id=self.trigger_id)
    #         .values_list("id", flat=True)
    #         .distinct()
    #     )

    # def _get_managers_of_all_branches(self):
    #     return User.objects.filter(
    #         Q(tenant=self.model_object.tenant)
    #         & (
    #             Q(role__name__in=[RoleName.OWNER.value, RoleName.CHAIN_MANAGER.value])
    #             | (
    #                 Q(role__name=RoleName.MANAGER.value)
    #                 & Q(
    #                     role__permission_group__in=PermissionGroup.objects.filter(
    #                         name="All Branch"
    #                     )
    #                 )
    #             )
    #         )
    #     ).values_list("id", flat=True)

    def _get_accountants(self):
        return list(User.objects.filter(
            role__name=RoleName.ACCOUNTANT.value,
            branch=self.model_object.branch,
        ).values_list("id", flat=True).distinct())

    def _add_notification(self, user_ids, action, message):
        notification_models = []
        for user_id in user_ids:
            notification_models.append(
                create_notification_model(
                    user_id,
                    self.category.id,
                    self.event.id,
                    message,
                    self.model_class.__name__,
                    self.model_object.id,
                ).id
            )
        if notification_models:
            self.notifications.append(
                {
                    "action": action,
                    "object": str(self.model_object.id),
                    "notifications": notification_models,
                    "message": message,
                    "category": self.category,
                }
            )
