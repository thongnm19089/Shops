import django.contrib.auth.password_validation as validators
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from ..models import BusinessUser

class BusinessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = "__all__"

class BusinessUserReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True, source="user.username")
    fullname = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    avatar_url = serializers.FileField(read_only=True)
    salary = serializers.IntegerField(read_only=True)
    color = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True, source="user.is_active")
    role = serializers.UUIDField(read_only=True, source="user.role_id")
    shift = serializers.UUIDField(read_only=True, source="user.shift_id")
    branch = serializers.UUIDField(read_only=True, source="user.branch_id")
    created_at = serializers.DateTimeField(read_only=True, source="user.created_at")
    is_block = serializers.BooleanField(read_only=True, source="user.is_block")
