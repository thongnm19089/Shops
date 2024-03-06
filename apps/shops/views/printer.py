from rest_framework import viewsets, status
from rest_framework import serializers
from core.mixins import GetSerializerClassMixin

from apps.users.models import User
from ..models.printer import Printer
from ..serializers.printer import PrinterSerializer, PrinterReadOnlySerializer

class PrinterViewSet(GetSerializerClassMixin,
                     viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
    serializer_action_classes = {
        'list': PrinterReadOnlySerializer,
        'retrieve': PrinterReadOnlySerializer,
    }
    # filter_class = PrinterFilterSet

    def get_queryset(self):
        queryset = self.queryset.all()
        user = self.request.user
        if isinstance(user, User) and not user.is_superuser:
            queryset = self.queryset.filter(branch=user.branch)
        return queryset
