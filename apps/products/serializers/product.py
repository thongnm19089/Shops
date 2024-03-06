from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .variant import VariantReadOnlySerializer
from .product_image import ProductImageWriteSerializer, ProductImageReadOnlySerializer
from .variant_option import VariantOptionReadOnlySerializer
from ..models import Product, VariantOption

class OptionWriteSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    keys = serializers.ListField(
        child=serializers.CharField(), required=True
    )



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageWriteSerializer(many=True, required=False)

    
    class Meta:
        model = Product
        exclude = ["landing_page_position", "landing_page_active"]
        
    def validate_name(self, name):
        if self.instance and self.instance.name == name:
            return name

        if Product.objects.filter(name=name).exists():
            raise serializers.ValidationError(_("Product with name {name} is existed").format(name=name))
        return name

    def validate_images(self, images):
        for image in images:
            if ('data:' or ';base64,') not in image['base64']:
                raise serializers.ValidationError(_("Invalid base64"))
        return images


class StockSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    branch = serializers.UUIDField(read_only=True, source="branch_id")


class ProductReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    # type = serializers.CharField(read_only=True)
    # price = serializers.IntegerField(read_only=True)
    # barcode = serializers.CharField(read_only=True)
    # sku = serializers.CharField(read_only=True)
    # duration = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)
    brand_id = serializers.UUIDField(read_only=True)
    brand_name = serializers.CharField(read_only=True, source="brand.name")
    position = serializers.IntegerField(read_only=True)
    category_id = serializers.UUIDField(read_only=True)
    category_name = serializers.CharField(read_only=True, source="category.name")
    # inventory = StockSerializer(
    #     read_only=True, many=True, source="inventory_set"
    # )
    status = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    images = ProductImageReadOnlySerializer(read_only=True, many=True, source="productimage_set")
    options = VariantOptionReadOnlySerializer(read_only=True, many=True, source="variantoption_set")
    variants = VariantReadOnlySerializer(read_only=True, many=True)


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        for index, option in enumerate(instance.variantoption_set.all(), 1):
            representation['option' + str(index)] = option.name
        return representation


class ProductRetrieveSerializer(ProductReadOnlySerializer):
    pass
    # sold_quantity = serializers.SerializerMethodField()
    # sold_avg_price = serializers.SerializerMethodField()

    # def get_sold_quantity(self, obj):
    #     quantity = obj.invoiceitem_set.filter(item_id=str(obj.id)).aggregate(total=Sum("quantity"))["total"]
    #     if not quantity:
    #         return 0
    #     return quantity

    # def get_sold_avg_price(self, obj):
    #     item = obj.invoiceitem_set.filter(item_id=str(obj.id)).aggregate(
    #         total_price=Sum(F("quantity") * F("price")),
    #         total=Sum("quantity"),
    #     )
    #     if not item["total_price"] or not item["total"]:
    #         return 0
    #     return item["total_price"] / item["total"]

  
class UpdatePositionSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    position = serializers.IntegerField(required=True)