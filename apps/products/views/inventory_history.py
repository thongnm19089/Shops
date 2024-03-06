from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.products.filters import InventoryHistoryFilterSet
from apps.products.models import (
    Inventory,
    InventoryHistory,
)
from apps.products.serializers import InventoryHistorySerializer, InventoryHistoryReadOnlySerializer
from core.mixins import GetSerializerClassMixin


class InventoryHistoryViewSet(
    GetSerializerClassMixin, viewsets.ModelViewSet
):
    # queryset = InventoryHistory.objects.filter(invoice__deleted__isnull=True).select_related("invoice").all()
    queryset = InventoryHistory.objects.all()
    http_method_names = ["post", "delete", "get"]
    serializer_class = InventoryHistorySerializer
    serializer_action_classes = {
        "list": InventoryHistoryReadOnlySerializer,
        "retrieve": InventoryHistoryReadOnlySerializer,
    }
    filterset_class = InventoryHistoryFilterSet
    
    def get_queryset(self):
        assert self.queryset is not None, (
            _("'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method.") % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        if hasattr(self.request, "user"):
            user = self.request.user
            if not user.is_superuser and not user.role.is_owner:
                queryset = queryset.filter(branch=user.branch)

        return queryset
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        v_data = serializer.validated_data
        
        quantity_adjust = v_data["quantity"]
        if v_data["is_exported"]:
            quantity_adjust = -1 * quantity_adjust
            
        with transaction.atomic():
            instance = serializer.save()
            
            inventory = Inventory.objects.select_for_update().get(
                product=v_data["product"],
                branch=v_data["branch"],
            )
            inventory.quantity += quantity_adjust
            
            instance.current_total = inventory.quantity
            
            instance.save()
            inventory.save()
            
        serializer = self.serializer_action_classes.get("retrieve")(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
