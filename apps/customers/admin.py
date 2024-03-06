from django.contrib import admin
from .models.customer import Customer

from .models.career import Career

class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code',
        'name',
        'phone',
        'email',
        'title',
        'gender',
        'address',
        'district',
        'city',
        'day_of_birth',
        'month_of_birth',
        'year_of_birth',
        'avatar_url',
        'facebook',
        'career',
        'note',
        # 'user_id',
        'created_at',
    ]

class CareerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Career, CareerAdmin)
