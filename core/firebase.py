import threading
from typing import Optional
from firebase_admin import messaging, credentials
import firebase_admin
# from coreapp.utils.logging_helper import get_log

# log = get_log()



cred = credentials.Certificate(
    "service_account.json"
)
firebase_admin.initialize_app(cred)

def sendPush(title, msg, registration_token, dataObject):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg,
        ),
        data=dataObject,
        tokens=registration_token
    )
    
    response = messaging.send_multicast(message)
    
    print("successfuly sent message", response)


