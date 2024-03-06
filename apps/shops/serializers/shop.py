from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        read_only_fields = ['slug_name', 'slug_name_index', 'created_at']
        fields = "__all__"
        # extra_kwargs = {
        #     "birthday_point": {"required": False},
        # }
        

class ShopReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug_name = serializers.CharField(read_only=True)
    slug_name_index = serializers.IntegerField(read_only=True)
    address = serializers.CharField(read_only=True)
    district = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.UUIDField(read_only=True)
    dayoff_allowed = serializers.IntegerField(read_only=True)
    hotline = serializers.CharField(read_only=True)
    logo_url = serializers.FileField(read_only=True)
    website_url = serializers.CharField(read_only=True)
    landing_page_title = serializers.CharField(read_only=True)
    copyright = serializers.CharField(read_only=True)
    owner_info = serializers.CharField(read_only=True)
