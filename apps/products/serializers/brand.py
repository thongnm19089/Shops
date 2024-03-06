from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import Brand
from core.mixins import TenantSerializerMixin


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"

    def validate_name(self, name):
        if self.instance and self.instance.name == name:
            return name

        if Brand.objects.filter(name=name).exists():
            raise serializers.ValidationError(_("Brand with name {name} is existed").format(name=name))
        return name


class BrandReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product_number = serializers.IntegerField(read_only=True)
