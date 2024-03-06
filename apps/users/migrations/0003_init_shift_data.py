# Manually created

from __future__ import unicode_literals
from django.db import migrations, models
import datetime


def init_shift_data(apps, schema_editor):
    Shift = apps.get_model("users", "Shift")
    Shift.objects.create(
        name="Mặc định",
        start_time=datetime.time(8, 0, 0),
        end_time=datetime.time(18, 0, 0),
        flexible_minutes=15,
    )

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_init_role_data')
    ]

    operations = [
        migrations.RunPython(init_shift_data),
    ]

