import logging
from apps.notifications.models import Notification
from apps.notifications.models.notification_event import NotificationEvent
from .base_service import BaseService
from .fcm import FCMService

FCM_CHANNEL = "fcm"

logger = logging.getLogger(__name__)


def get_notification_config(channel):
    config = {
        "channel": channel,
    }
    if channel == FCM_CHANNEL:
        return config
    else:
        raise Exception("NOT SUPPORTED")

    
def get_notification_service(config):
    channel = config.get("channel", "")
    service = None
    if channel == FCM_CHANNEL:
        service = FCMService(config)
    else:
        raise Exception("NOT SUPPORTED")

    if not isinstance(service, BaseService):
        raise Exception("Must implement BaseService method")

    return service

def create_notification_event_model(model, obj_id, action, category_id, trigger_id):
    event = NotificationEvent(
        model=model,
        action=action,
        category_id=str(category_id),
    )
    if obj_id:
        event.model_id = str(obj_id)
    if trigger_id:
        event.trigger_id = str(trigger_id)
    event.save()
    return event

def create_notification_model(user_id, category_id, event_id, content, model=None, model_id=None):
    notification = Notification(
        user_id=str(user_id),
        category_id=str(category_id),
        event_id=str(event_id),
        content=content,
    )
    if model and model_id:
        notification.model = model
        notification.model_id = str(model_id)
    notification.save()
    return notification
