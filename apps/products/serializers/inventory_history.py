from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models.inventory_history import InventoryHistory
from core.mixins import TenantSerializerMixin
from ..models.inventory import Inventory
from apps.shops.models import Branch


class InventoryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryHistory
        exclude = ["current_total"]
        extra_kwargs = {
            "branch": {"required": False},
            "user": {"required": False},
        }
        
    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        if hasattr(self.context["request"], "user"):
            ret["user"] = self.context["request"].user
            if Branch.objects.filter(is_active=True).count() == 1:
                ret["branch"] = Branch.objects.get(is_active=True)

        return ret


    def validate(self, data):
        if "branch" not in data:
            raise serializers.ValidationError(
                _("Branch must be specified")
            )
        inventory = Inventory.objects.filter(
            product=data["product"],
            branch=data["branch"],
        )
        
        if not inventory.exists():
            raise serializers.ValidationError(
                _("Product does not exist in this branch")
            )
 
        if data["is_exported"]:
            if data["reason"].startswith("I_"):
                raise serializers.ValidationError(
                    _("Reason must be export reason")
                )
            print("ssssssss", data["quantity"])
            if (int(data["quantity"]) <= 0):
                raise serializers.ValidationError(_("Quantity must be positive integer"))

            if inventory.get().quantity <= 0:
                raise serializers.ValidationError(_("Không còn sản phẩm nào trong kho"))

            if int(data["quantity"]) >= inventory.get().quantity:
                raise serializers.ValidationError(
                    _("Số lượng tồn kho không đủ")
                )

            return data

        if data["reason"].startswith("E_"):
            raise serializers.ValidationError(_("Reason must be import reason"))
        return data
    

class InventoryHistoryReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    inventory = serializers.UUIDField(read_only=True, source="inventory_id")
    user = serializers.UUIDField(read_only=True, source="user_id")
    is_exported = serializers.BooleanField(read_only=True)
    reason = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    current_total = serializers.IntegerField(read_only=True)
    # invoice = serializers.UUIDField(read_only=True, source="invoice_id")
    # invoice_code = serializers.UUIDField(read_only=True, source="invoice.code")
    branch = serializers.UUIDField(read_only=True, source="branch_id")
    # tenant = serializers.UUIDField(read_only=True, source="tenant_id")
    created_at = serializers.DateTimeField(read_only=True)

