import logging

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.users.models import Device, Token
from apps.users.serializers import (
    UserDeviceReadOnlySerializer,
    RegisterDeviceSerializer,
)

logger = logging.getLogger(__name__)

class DeviceView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Devices",
        responses={200: UserDeviceReadOnlySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        # Get all device by user
        user = request.user
        tokens = Token.objects.filter(user=user)
        serializer = UserDeviceReadOnlySerializer(tokens, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Register Device",
        request_body=RegisterDeviceSerializer,
        responses={200: RegisterDeviceSerializer()},
    )
    def post(self, request):
        # register device token
        user = request.user
        serializer = RegisterDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        device = Device.objects.filter(token=data["token"])

        with transaction.atomic():
            if device and device.get().user_id == user.id:
                device.update(is_active=data["is_active"])
            else:
                Device.objects.filter(token=data["token"]).delete()
                Device.objects.create(
                    user=user,
                    token=data["token"],
                    is_active=data["is_active"],
                    os=serializer.validated_data["os"],
                )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    
