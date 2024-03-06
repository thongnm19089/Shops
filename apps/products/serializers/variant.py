from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import Variant
from .product_image import ProductImageReadOnlySerializer


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"

    def validate(self, data):
        if self.instance and (self.instance.name == data["name"] and self.instance.product == data["product"]):
            return data

        if Variant.objects.filter(name=data["name"], product=data["product"]).exists():
            raise serializers.ValidationError(_("Variant name {name} of product {product} is existed").format(name=data["name"], product=data["product"]))
        return data


class VariantReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    barcode = serializers.CharField(read_only=True)
    sku = serializers.CharField(read_only=True)
    images = ProductImageReadOnlySerializer(read_only=True, many=True, source="productimage_set")
    position = serializers.IntegerField(read_only=True)
    product_id = serializers.UUIDField(read_only=True)
    sellable = serializers.BooleanField(read_only=True)
    # variant_price = serializers.CharField()