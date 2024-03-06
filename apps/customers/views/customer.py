import json
import logging
from datetime import datetime, timedelta

from django.db import transaction, connection
from django.db.models import Sum, F, Q, Prefetch
from django.db.models.query import QuerySet
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import APIException, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from apps.customers.models import customer

from apps.customers.filters import CustomerFilterSet
from apps.users.models import User, RoleName, Token
from apps.users.serializers import UserSerializer
from apps.customers.models import (
    Customer,
    Career,
)
from apps.customers.models.customer import Gender
from apps.customers.serializers import (
    CustomerSerializer,
    CustomerReadOnlySerializer,
    CustomerProfileSerializer,
    CustomerEditProfileSerializer,
)
# from apps.customers.serializers.career import CareerReadOnlySerializer
from core.cache import custom_cache_response
# from core.exporter import Exporter
from core.mixins import GetSerializerClassMixin, GetPermissionClassMixin, CustomCacheResponseMixin
from core.permissions import (
    UserRolePermission,
    CustomerUserPermission,
    BusinessUserPermission,
)
from core.util import get_generated_index
from rest_framework.parsers import MultiPartParser, FormParser

logger = logging.getLogger(__name__)


class CustomerViewSet(
    CustomCacheResponseMixin,
    GetSerializerClassMixin,
    GetPermissionClassMixin,
    viewsets.ModelViewSet
):
    queryset = Customer.objects.prefetch_related(
        'branches',
    ).order_by('-created_at')
    serializer_class = CustomerSerializer
    serializer_action_classes = {
        "list": CustomerReadOnlySerializer,
        "retrieve": CustomerReadOnlySerializer,
    }
    permission_classes = [IsAuthenticated, UserRolePermission]
    permission_classes_by_action = {
        'list': [BusinessUserPermission],
        'update': [BusinessUserPermission],
    }
    http_method_names = ["get", "put"]
    parser_classes = (FormParser, MultiPartParser,)
    filterset_class = CustomerFilterSet

    @swagger_auto_schema(
        operation_description="Admin Update customer's profile",
        request_body=CustomerProfileSerializer,
        responses={200: (CustomerReadOnlySerializer)},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        
        user_obj = instance.user
        serializer = CustomerProfileSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        
        user_serializer = UserSerializer(
            user_obj,
            data=request.data,
            partial=partial,
            context={'user': request.user}
        )
        user_serializer.is_valid(raise_exception=True)
        
        customer_serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        customer_serializer.is_valid(raise_exception=True)
        
        user_obj = instance.user

        with transaction.atomic():            
            user_serializer.save()
            customer_serializer.save()
            
            if "password" in user_serializer.validated_data:
                Token.objects.filter(user=user_obj).delete()
                
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        instance.refresh_from_db()
        serializer = self.serializer_action_classes.get("retrieve")(instance)
        
        return Response(serializer.data)


    @swagger_auto_schema(
        operation_description="Show customer's profile",
        request_body=None,
        responses={200: (CustomerReadOnlySerializer)},
    )
    @action(
        methods=["GET"],
        detail=False,
        url_path="me",
        url_name="me",
        filterset_class=None,
        permission_classes=[IsAuthenticated, CustomerUserPermission],
        pagination_class=None,
    )
    def me(self, request, *args, **kwargs):
        user = request.user

        serializer = self.serializer_action_classes.get("retrieve")(
            user.customer_set.first()
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_description="Update customer's profile",
        request_body=CustomerEditProfileSerializer,
        responses={200: (CustomerReadOnlySerializer)},
    )
    @action(
        methods=["PUT"],
        detail=False,
        url_path="update_profile",
        url_name="update_profile",
        # filterset_class=None,
        permission_classes=[IsAuthenticated, CustomerUserPermission],
        pagination_class=None,
    )
    def update_profile(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        
        user_obj = request.user
        customer_obj = user_obj.customer_set.first()
        serializer = CustomerEditProfileSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        
        user_serializer = UserSerializer(
            user_obj,
            data=request.data,
            partial=partial,
            context={'user': request.user}
        )
        user_serializer.is_valid(raise_exception=True)
        
        customer_serializer = self.get_serializer(
            customer_obj, data=request.data, partial=partial
        )
        customer_serializer.is_valid(raise_exception=True)

        with transaction.atomic():            
            user_serializer.save()
            customer_serializer.save()

            if "password" in user_serializer.validated_data:
                Token.objects.filter(user=user_obj).delete()
                
        if getattr(customer_obj, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            customer_obj._prefetched_objects_cache = {}
        customer_obj.refresh_from_db()
        serializer = self.serializer_action_classes.get("retrieve")(customer_obj)
        
        return Response(serializer.data)
