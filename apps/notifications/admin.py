from django.contrib import admin

from .models import Notification, NotificationSetting, NotificationCategory


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'content', 'state', 'delivery_at', 'created_at', 'branch']


class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'enabled', 'created_at']


class NotificationCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']


admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationSetting, NotificationSettingAdmin)
admin.site.register(NotificationCategory, NotificationCategoryAdmin)
