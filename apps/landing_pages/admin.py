from django.contrib import admin

from .models import LandingPageImage, LandingPageTime


class LandingPageImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "url",
        "type",
        "created_at",
    ]

class LandingPageTimeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "start_time",
        "end_time",
        "day_of_week",
        "is_active",
        "created_at",
    ]

admin.register(LandingPageImage, LandingPageImageAdmin)
admin.register(LandingPageTime, LandingPageTimeAdmin)