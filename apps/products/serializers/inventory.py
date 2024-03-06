from rest_framework import serializers
from django.core.paginator import Paginator


from ..models.inventory import Inventory
from core.mixins import TenantSerializerMixin


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class _ProductReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)


class InventoryReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    product = _ProductReadOnlySerializer(read_only=True)
    current_total = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    branch = serializers.UUIDField(read_only=True, source="branch_id")
    created_at = serializers.DateTimeField(read_only=True)

