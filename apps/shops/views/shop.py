from rest_framework import viewsets, status
from rest_framework.response import Response
from core.mixins import GetSerializerClassMixin, GetPermissionClassMixin, CustomCacheResponseMixin
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.users.models import RoleName
from ..models import Shop
from ..serializers.shop import ShopSerializer, ShopReadOnlySerializer
from core.decorator import query_debugger
from apps.notifications.handlers.constants import (
    SHOP_UPDATE_ACTION,
)
from apps.notifications.tasks import process_notification


class ShopViewSet(CustomCacheResponseMixin,
                    GetSerializerClassMixin,
                    GetPermissionClassMixin,
                    viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    serializer_action_classes = {
        'list': ShopReadOnlySerializer,
        'retrieve': ShopReadOnlySerializer,
    }
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [AllowAny]
    }
    http_method_names = ["get", "put", "patch"]

    def get_queryset(self):
        queryset = self.queryset.all()
        user = self.request.user
        if user.is_superuser:
            return queryset

        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        process_notification.apply_async(
            args=(SHOP_UPDATE_ACTION, instance.id, self.request.user.id)
        )

        return Response(serializer.data, status=status.HTTP_200_OK)