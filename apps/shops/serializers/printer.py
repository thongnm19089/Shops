from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.mixins import TenantSerializerMixin
from ..models.printer import Printer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = "__all__"
        extra_kwargs = {
            "branch": {"required": False},
        }

    def to_internal_value(self, data):
        ret = super(PrinterSerializer, self).to_internal_value(data)
        user = self.context["request"].user
        if not ret.get("branch"):
            ret["branch"] = user.branch
        return ret

    def validate_branch(self, branch_id):
        user = self.context["request"].user
        if (
            branch_id != user.branch_id
            and not user.is_superuser
            and not user.role.has_branches_permission
        ):
            raise serializers.ValidationError(
                _("You do not have permission on branch {branch}").format(
                    branch=branch_id
                )
            )
        return branch_id

    def validate(self, data):
        ip = data.get("ip")
        branch = data.get("branch")
        if ip and (
            (self.instance and self.instance.ip != ip) or not self.instance
        ) and Printer.objects.filter(ip=ip, branch_id=branch.id).exists():
            raise serializers.ValidationError(_("This ip is already exists"))
        return data


class PrinterReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    ip = serializers.CharField(read_only=True)
    tenant = serializers.UUIDField(read_only=True, source="tenant_id")
    branch = serializers.UUIDField(read_only=True, source="branch_id")
    note = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
