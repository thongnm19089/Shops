from __future__ import unicode_literals

from django.db import migrations


def init_notification_category_data(apps, schema_editor):
    category_names = [
        'Daily reports',
        'Password changed',
        'Shop update',
        'User block status changed',
        'User role changed',
        'Invoice',
        'Checkin success',
        'Checkin reminding',
        'User shift changed',
        'Shift update',
    ]
    NotificationCategory = apps.get_model("notifications", "NotificationCategory")
    for name in category_names:
        category = NotificationCategory()
        category.name = name
        category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('notifications', '0001_initial')
    ]

    operations = [
        migrations.RunPython(init_notification_category_data),
    ]
