# Manually created

from __future__ import unicode_literals
from django.db import migrations, models


def init_branch_data(apps, schema_editor):
    Branch = apps.get_model("shops", "Branch")
    Branch.objects.create(
        name="Minh xù",
        slug_name="Minh xù",
        address="180 Minh Khai",
        district="Hai Bà Trưng",
        city="Hà nội",
        root_branch=True,
    )

class Migration(migrations.Migration):
    dependencies = [
        ('shops', '0002_init_shop_data')
    ]

    operations = [
        migrations.RunPython(init_branch_data),
    ]

