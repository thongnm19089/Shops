from django.contrib import admin
from .models import (
    Shop,
    Branch,
    Printer,
)


class ShopAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug_name',
        'address',
        'district',
        'city',
        'is_active',
        "hotline",
        "logo_url",
        "dayoff_allowed",
    ]


class BranchAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug_name',
        'address',
        'district',
        'city',
        'root_branch',
        'is_active',
    ]



class PrinterAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip', 'branch',
                    'note', ]

admin.site.register(Shop, ShopAdmin)
admin.site.register(Printer, PrinterAdmin)
admin.site.register(Branch, BranchAdmin)
