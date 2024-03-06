import uuid

from django.db import models
from rest_framework.authtoken.models import Token as BaseToken
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class Token(BaseToken):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    device_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'token'
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def __str__(self):
        return str(self.key)
