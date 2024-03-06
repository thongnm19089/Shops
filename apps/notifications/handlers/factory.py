from . import HANDLERS


class NotificationFactory:
    handlers = HANDLERS

    def __init__(self, action, obj_id, trigger_id):
        self.obj_id = obj_id
        self.trigger_id = trigger_id
        self.action = action

    def create_notifications(self):
        klass = self.handlers[self.action]
        handler = klass(self.obj_id, self.trigger_id, self.action)
        notifications = handler.create_notifications()
        return notifications
