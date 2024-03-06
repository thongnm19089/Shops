import uuid
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _

# from apps.users.models import PermissionGroup
# from .permission import Permission


class RoleName(Enum):
    SALE_STAFF = 'Sale Staff'
    RECEPTIONIST = 'Receptionist'
    ACCOUNTANT = 'Accountant'
    MANAGER = 'Manager'
    OWNER = 'Owner'
    CUSTOMER = 'Customer'


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    # permission = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('role permission')
    # )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "role"
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_role_name"
            ),
        ]
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def is_sale_staff(self):
        return self.name == RoleName.SALE_STAFF.value

    @property
    def is_receptionist(self):
        return self.name == RoleName.RECEPTIONIST.value

    @property
    def is_accountant(self):
        return self.name == RoleName.ACCOUNTANT.value

    @property
    def is_manager(self):
        return self.name == RoleName.MANAGER.value

    @property
    def is_owner(self):
        return self.name == RoleName.OWNER.value

    @property
    def is_customer(self):
        return self.name == RoleName.CUSTOMER.value
        
    @property
    def has_manager_permission(self):
        return self.name in [RoleName.OWNER.value, RoleName.MANAGER.value]
