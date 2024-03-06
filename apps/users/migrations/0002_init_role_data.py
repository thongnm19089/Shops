# Manually created

from __future__ import unicode_literals
from django.db import migrations, models
from apps.users.models import RoleName


def init_role_data(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    default_role_names = [
        RoleName.OWNER.value,
        RoleName.MANAGER.value,
        RoleName.ACCOUNTANT.value,
        RoleName.RECEPTIONIST.value,
        RoleName.SALE_STAFF.value,
        RoleName.CUSTOMER.value,
    ]
    roles = []
    for name in default_role_names:
        roles.append(
            Role(
                name=name
            )
        )

    Role.objects.bulk_create(roles)

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial')
    ]

    operations = [
        migrations.RunPython(init_role_data),
    ]

