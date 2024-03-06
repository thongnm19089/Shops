import abc

class BaseService(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'handle_notification') and 
                callable(subclass.handle_notification) and 
                hasattr(subclass, 'send_notification') and 
                callable(subclass.send_notification))
