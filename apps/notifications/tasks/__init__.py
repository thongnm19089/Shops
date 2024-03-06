import datetime

from apps.notifications.handlers import NotificationFactory
from apps.notifications.handlers.constants import (
    BIRTHDAY_REMINDING_ACTION,
)
from apps.notifications.models.notification import Notification, NotificationState
from apps.customers.models import Customer 
from config import celery_app
from core.celery_task_base import BaseTask
from core.notification import (
    get_notification_config,
    FCM_CHANNEL,
    get_notification_service,
)
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def process_send_notification(channel, notifications):
    for notification in notifications:
        config = get_notification_config(FCM_CHANNEL)
        notification_service = get_notification_service(config)
        payload = notification_service.handle_notification(notification)
        if not payload:
            logger.info(f'No device found')
            continue
        logger.info(f'start to send {len(payload)} messages to firebase')
        send_notifications(notification_service, payload)

def send_notifications(notification_service, payload: dict):
    resp = notification_service.send_notification(payload)
    if resp.get("succeed"):
        logger.info(f"Succeed notifications: {len(resp['succeed'])}")
        Notification.objects.filter(pk__in=resp["succeed"]).update(
            state=NotificationState.DELIVERED, delivery_at=datetime.datetime.now()
        )

    if resp.get("failed"):
        fail_msg = []
        for id, token_list in resp["failed"].items():
            fail_msg.append('Notification {} failed with: {}'.format(id, ", ".join(token_list)))
        logger.info("\n".join(fail_msg))


@celery_app.task(base=BaseTask)
def process_notification(action, obj_id, trigger_id):
    logger.info(f'Received task action={action}, obj={obj_id}, trigger={trigger_id}')
    notifications = NotificationFactory(action, obj_id, trigger_id).create_notifications()

    # send notification
    if notifications:
        process_send_notification(FCM_CHANNEL, notifications)
    else:
        logger.debug('Nothing to send')
        
        
@celery_app.task(base=BaseTask)
def daily_birthday_reminder():
    logger.info('Start set birthday reminder')
    notifications = []
    today = datetime.date.today()
    customers = Customer.objects.filter(
        month_of_birth=today.month,
        day_of_birth=today.day
    ).values_list("id", flat=True)
    for customer in customers:
        notifications.extend(
            NotificationFactory(
                BIRTHDAY_REMINDING_ACTION,
                customer,
                None
            ).create_notifications()
        )
    if notifications:
        process_send_notification(FCM_CHANNEL, notifications)
    else:
        logger.debug('Nothing to send')
