from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import VariantOption


class VariantOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantOption
        fields = "__all__"

    def validate(self, data):
        if self.instance and (self.instance.name == data["name"] and self.instance.product == data["product"]):
            return data

        if VariantOption.objects.filter(name=data["name"], product=data["product"]).exists():
            raise serializers.ValidationError(_("Variant Option with name {name} of product {product} is existed").format(name=data["name"], product=data["product"]))
        return data


class VariantOptionReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    position = serializers.IntegerField(read_only=True)
    values = serializers.ListField(child=serializers.CharField(), read_only=True)