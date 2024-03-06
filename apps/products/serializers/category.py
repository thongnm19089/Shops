from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["landing_page_position", "landing_page_active"]

    def validate_name(self, name):
        if self.instance and self.instance.name == name:
            return name

        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError(_("Category with name {name} is existed").format(name=name))
        return name


class CategoryReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)
    product_number = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    position = serializers.IntegerField(read_only=True)
