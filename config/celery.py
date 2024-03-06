from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
app = Celery("shops")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Ho_Chi_Minh'
app.conf.broker_transport_options = {'visibility_timeout': 3600 * 24}

app.conf.beat_schedule = {
    "daily_birthday_reminder": {
        "task": "apps.notifications.tasks.daily_birthday_reminder",
        "schedule": crontab(),
    },
}

