from rest_framework import viewsets
from django.db.models import Count
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.products.models import Brand
from apps.products.serializers import BrandSerializer, BrandReadOnlySerializer
from core.mixins import GetSerializerClassMixin, GetPermissionClassMixin
from core.permissions import (
    BusinessUserPermission,
)


class BrandViewSet(
    GetSerializerClassMixin, GetPermissionClassMixin, viewsets.ModelViewSet
):
    queryset = Brand.objects.annotate(product_number=Count("products")).order_by('-created_at')
    serializer_class = BrandSerializer
    serializer_action_classes = {
        "list": BrandReadOnlySerializer,
        "retrieve": BrandReadOnlySerializer,
    }
    permission_classes = [BusinessUserPermission]
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
    }
