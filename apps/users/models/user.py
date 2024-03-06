import uuid
from datetime import datetime, timedelta

import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db.models import Q
import slugify

from .user_manager import CustomUserManager
from .shift import Shift
from .role import Role
from ...shops.models import Branch

class User(AbstractBaseUser):
    USERNAME_FIELD = "username"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=150, unique=True, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_block = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def token(self):
        return self._generate_jwt_token()

    def clean(self):
        super().clean()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return (
            self.username
            # if self.username
            # else "{}-{}".format(self.fullname, self.phone)
        )

    class Meta:
        db_table = "user"
        ordering = ["created_at"]

    # def save(self, *args, **kwargs):
    #     self.ascii_name = slugify.slugify(self.fullname, separator=" ")
    #     super(User, self).save(*args, **kwargs)

    def _generate_jwt_token(self):
        iat = datetime.now()
        exp = iat + timedelta(days=60)
        payload = {
            "id": str(self.id),
            "fullname": self.customer_set.first().name,
            "phone": self.customer_set.first().phone,
            "exp": exp,
            "iat": iat,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")

# activity_log.register(User, redact_fields=["password"], exclude_fields=["last_login", "ascii_name"])