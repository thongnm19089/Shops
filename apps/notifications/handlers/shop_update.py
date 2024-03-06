from django.db.models import Q

from apps.users.models import User, RoleName
from apps.shops.models import Shop
from custom.translation import CustomTranslation
from . import constants
from .handler import Handler

translation = CustomTranslation()


class ShopUpdateHandler(Handler):
    model_class = Shop
    category_name = "Shop update"

    @classmethod
    def name(cls):
        return constants.SHOP_UPDATE_ACTION

    def get_receivers(self):
        receivers = User.objects.filter(
            Q(
                role__name__in=[
                    RoleName.OWNER.value,
                    RoleName.MANAGER.value,
                    RoleName.ACCOUNTANT.value,
                    RoleName.RECEPTIONIST.value,
                    RoleName.SALE_STAFF.value,
                ]
            )
        ).values_list("id", flat=True)
        return receivers

    def create_notifications(self):
        message = translation.gettext("SHOP_UPDATE_MSG").format(
            shop=self.model_object.name
        )
        # receivers = self.get_receivers()
        receivers = set(User.objects.filter(
            # tenant=self.model_object,
            # role__name=RoleName.OWNER.value).exclude(id=self.trigger_id).values_list('id', flat=True))
            # role__name=RoleName.OWNER.value).exclude(id=self.trigger_id).values_list('id', flat=True))
            role__name=RoleName.OWNER.value).values_list('id', flat=True))
        self._add_notification(receivers, constants.SHOP_UPDATE_ACTION, message)

        return self.notifications
