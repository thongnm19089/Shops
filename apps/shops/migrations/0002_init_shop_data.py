# Manually created

from __future__ import unicode_literals
from django.db import migrations, models


def init_shop_data(apps, schema_editor):
    Shop = apps.get_model("shops", "Shop")
    Shop.objects.create(
        name="Minh xù",
        slug_name="Minh xù",
    )

class Migration(migrations.Migration):
    dependencies = [
        ('shops', '0001_initial')
    ]

    operations = [
        migrations.RunPython(init_shop_data),
    ]

