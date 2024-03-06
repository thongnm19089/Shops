from rest_framework import serializers
from apps.users.models.device import DeviceOS


class UserDeviceReadOnlySerializer(serializers.Serializer):
    device_name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, source="created")


class RegisterDeviceSerializer(serializers.Serializer):
    os = serializers.ChoiceField(choices=DeviceOS.choices, required=True)
    token = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)
