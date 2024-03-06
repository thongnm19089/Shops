import json
import os
import logging

import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.messaging import UnregisteredError

from apps.users.models import User, Device

logger = logging.getLogger(__name__)


class FCMService:
    def __init__(self, config):
        path = config.get(
            "path", os.getenv("CREDENTIAL_PATH", "./service_account.json")
        )
        cred = credentials.Certificate(path)
        try:
            self.app = firebase_admin.get_app()
        except:
            self.app = firebase_admin.initialize_app(credential=cred)
            
    def handle_notification(self, notification):
        notification_ids = notification.get("notifications")
        # category = notification.get("category")

        users = User.objects.filter(
            devices__is_active=True,
            # devices__deleted__isnull=True,
            notification__id__in=notification_ids,
            # notificationsetting__category=category,
            # notificationsetting__enabled=True,
        ).values("devices__token", "notification", "id")

        if len(users) == 0:
            return None
        
        payload_list = []
        for user in users:
            payload = {
                "notification": user["notification"],
                "token": user["devices__token"],
                "title": "SPAGO",
                "body": notification.get("message"),
                "action": notification.get("action", ""),
                "object": str(notification.get("object", "")),
            }
            payload_list.append(payload)
            
        return payload_list
                    
    def send_notification(self, payload):
        succeed = []
        failed = dict()
        unregistered_token = []
        
        if not isinstance(payload, list):
            payload = [payload]
            
        for data in payload:
            token = data.get("token")
            
            notification = messaging.Notification(
                title=data.get("title"),
                body=data.get("body"),
            )
            
            notify_data = {
                "action": data.get("action") if data.get("action") else "",
                "object": data.get("object") if data.get("object") else "",
                "data": json.dumps(data.get("data", "")),
            }

            message = messaging.Message(
                token=token, notification=notification, data=notify_data
            )
            
            try:
                messaging.send(message=message, app=self.app)
                succeed.append(data.get("notification"))
            except UnregisteredError:
                unregistered_token.append(token)
                logger.exception(f"Token {token} raises UnregisteredError")
            except Exception as ex:
                logger.exception(ex)
            finally:
                if not failed.get(data.get("notification")):
                        failed[data.get("notification")] = []
                failed[data.get("notification")].append(token)
                
        if unregistered_token:
            # deactivate UnregisteredError token
            Device.objects.filter(token__in=unregistered_token).update(is_active=False)

        return {
            "succeed": succeed,
            "failed": failed,
        }