# Generated by Django 3.0.7 on 2020-08-20 03:09

from django.db import migrations, models


def migrate_notification_category(apps, schema_editor):
    NotificationCategory = apps.get_model("notifications", "NotificationCategory")
    NotificationCategory.objects.create(
        name='birthday reminding'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_migrate_notification_setting'),
    ]

    operations = [
        migrations.RunPython(migrate_notification_category),
    ]
