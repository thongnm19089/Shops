from apps.notifications.handlers.constants import BIRTHDAY_REMINDING_ACTION
from apps.users.models import Shift, User
from apps.customers.models import Customer
from custom.translation import CustomTranslation
from . import constants
from .handler import Handler

translation = CustomTranslation()


class BirthdayRemindingHandler(Handler):
    model_class = Customer
    category_name = "birthday reminding"

    @classmethod
    def name(cls):
        return constants.BIRTHDAY_REMINDING_ACTION

    def create_notifications(self):
        message = translation.gettext("BIRTHDAY_REMINDING").format(
            customer=self.model_object.name
        )
        customer = Customer.objects.filter(id=self.model_object.id)
        print("aaaaaaaa", customer)
        if customer:
            users = User.objects.filter(
                id=customer[0].user.id,
                notificationsetting__category__name=self.category_name,
                notificationsetting__enabled=True,
            ).values_list("id", flat=True)
            print("bbbbbbbbb", users)
            self._add_notification(users, BIRTHDAY_REMINDING_ACTION, message)

        return self.notifications
