from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from ..models.branch import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        extra_kwargs = {
            "district": {"required": False},
            "city": {"required": False}
        }

    def validate_name(self, name):
        user = self.context["request"].user
        if self.instance and self.instance.name == name:
            return name
        if not user.is_superuser and Branch.objects.filter(name=name).exists():
            raise serializers.ValidationError(_('Branch with name {name} is already existed').format(name=name))
        return name


class BranchReadOnySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug_name = serializers.SlugField(read_only=True)
    address = serializers.CharField(read_only=True)
    district = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    root_branch = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
