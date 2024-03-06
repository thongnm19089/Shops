from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.products.filters import InventoryHistoryFilterSet
from apps.products.models import Inventory
from apps.products.serializers import InventoryReadOnlySerializer
from core.mixins import GetSerializerClassMixin


class InventoryViewSet(
    GetSerializerClassMixin, viewsets.ModelViewSet,
):
    queryset = Inventory.objects.all().select_related("product")
    http_method_names = ["get"]
    serializer_action_classes = {
        "list": InventoryReadOnlySerializer,
        "retrieve": InventoryReadOnlySerializer,
    }
    
