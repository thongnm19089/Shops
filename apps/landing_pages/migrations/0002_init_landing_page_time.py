# Manually created

from __future__ import unicode_literals
from django.db import migrations, models
import apps.landing_pages.constant as constant


def init_landing_page_time_setting(apps, schema_editor):
    LandingPageTime = apps.get_model("landing_pages", "LandingPageTime")
    time_data = []
    for day_of_week in range(2, 9):
        time_setting = LandingPageTime(
            start_time=constant.DEFAULT_START_TIME,
            end_time=constant.DEFAULT_END_TIME,
            is_active=True,
            day_of_week=day_of_week,
        )
        time_data.append(time_setting)
    LandingPageTime.objects.bulk_create(time_data)


class Migration(migrations.Migration):
    dependencies = [
        ('landing_pages', '0001_initial')
    ]

    operations = [
        migrations.RunPython(init_landing_page_time_setting),
    ]

