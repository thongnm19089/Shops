from .vi import messages as vi_messages

DEFAULT_LOCALE = "vi"

locale_message_mapping = {
    DEFAULT_LOCALE: vi_messages.messages
}

class CustomTranslation:
    def __init__(self, locale=None):
        self.locale = DEFAULT_LOCALE 
        if locale:
            self.locale = locale
        self.messages = locale_message_mapping[self.locale]

    def gettext(self, key):
        return self.messages.get(key, key)
