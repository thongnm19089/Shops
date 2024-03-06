from django.contrib import admin

from apps.marketings.models import CeleryTask


class CeleryTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'celery_task_id', 'content']
    

admin.site.register(CeleryTask, CeleryTaskAdmin)
    