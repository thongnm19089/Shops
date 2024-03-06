from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.mixins import GetSerializerClassMixin, GetPermissionClassMixin, CustomCacheResponseMixin
from ..serializers.branch import BranchSerializer, BranchReadOnySerializer
from ..models.branch import Branch


class BranchViewSet(CustomCacheResponseMixin,
                    GetSerializerClassMixin,
                    GetPermissionClassMixin,
                    viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    serializer_action_classes = {
        'list': BranchReadOnySerializer,
        'retrieve': BranchReadOnySerializer,
    }
    permission_classes_by_action = {
        'list': [AllowAny],
    }

