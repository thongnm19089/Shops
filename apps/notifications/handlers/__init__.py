from .shop_update import ShopUpdateHandler
from .birthday_reminding import BirthdayRemindingHandler

handler_classess = [
    ShopUpdateHandler,
    BirthdayRemindingHandler,
]

HANDLERS = {
    h.name(): h for h in handler_classess
}

from .factory import NotificationFactory
