import os
from django.contrib import admin
from django.conf import settings
from .models import (
    Brand,
    Category,
    Product,
    Variant,
    VariantOption,
    ProductImage,
    Inventory,
    InventoryHistory,
)

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "color",
        "description",
        "position",
        "landing_page_position",
        "landing_page_active",
    ]
    

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.safestring import mark_safe
        if obj.image_url:
            image_url = settings.MEDIA_URL + str(obj.image_url)
            if os.path.isfile(os.path.join("media", str(obj.image_url))):
                return mark_safe('<img src="{}" width="200px" height="auto" />'.format(image_url))
        return 'No image'


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        # "price",
        # "barcode",
        # "sku",
        "brand",
        "position",
        "landing_page_position",
        "landing_page_active",
        "category",
        # "show_url",
    ]

    # fields = ( 'show_url',)
    # readonly_fields = ('show_url',)
    # def show_url(self, obj):
    #     from django.utils.html import format_html
    #     if obj.image_url:
    #         return format_html(f'<img src="{settings.MEDIA_URL + str(obj.image_url)}" width="200px" height="auto" />')
    #     return None

    # show_url.short_description = 'Image'
    # show_url.allow_tags = True
    # inlines = [ProductImageInline,]


class VariantOptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_id",
        "name",
        "values",
        "position",
    ]
    

class VariantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_id",
        "name",
        "sku",
        "barcode",
        "price",
        "brand_id",
        "category_id",
    ]
    

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product",
        "path",
    ]
    # model = ProductImage
    # pass


class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_id",
        "quantity",
        "branch_id",
    ]


class InventoryHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product",
        "user",
        # "invoice",
        "quantity",
        "current_total",
        "is_exported",
        "reason",
        "branch",
    ]


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(VariantOption, VariantOptionAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(InventoryHistory, InventoryHistoryAdmin)
