from django.contrib import admin
from .models import (
    Role,
    Shift,
    User,
    BusinessUser,
    Device,
    Token,
)


class AppUserAdmin(admin.ModelAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    list_display = [
        "id",
        "username",
    ]
    list_filter = ["is_superuser", "is_active"]
    filter_horizontal = []
    

class BusinessUserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "fullname",
    ]


class RoleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]

class ShiftAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]

class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'is_active', 'user']

class TokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user', 'device_name']

admin.site.register(User, AppUserAdmin)
admin.site.register(BusinessUser, BusinessUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Token, TokenAdmin)

