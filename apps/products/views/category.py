from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from django.db.models import Count, F, Q
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException


from apps.products.models import Category
from apps.products.serializers import (
    CategorySerializer,
    CategoryReadOnlySerializer,
)
from apps.products.serializers.product import UpdatePositionSerializer
from core.mixins import GetSerializerClassMixin, GetPermissionClassMixin
from core.permissions import (
    BusinessUserPermission,
)


class CategoryViewSet(
    GetSerializerClassMixin, GetPermissionClassMixin, viewsets.ModelViewSet
):
    queryset = Category.objects.annotate(
        product_number=Count("products")
    ).order_by(F("position").asc(nulls_first=True), "-created_at")
    
    serializer_class = CategorySerializer
    serializer_action_classes = {
        "list": CategoryReadOnlySerializer,
        "retrieve": CategoryReadOnlySerializer,
    }
    permission_classes = [BusinessUserPermission]
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
    }


    @swagger_auto_schema(
        query_serializer=UpdatePositionSerializer,
        request_body=UpdatePositionSerializer, responses={200: None,}
    )
    @action(
        methods=["PUT"],
        detail=False,
        url_path="update_position",
        url_name="update_position",
    )
    def update_position(self, request, *args, **kwargs):
        serializer = UpdatePositionSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        user = request.user
        ids = []
        position_dict = dict()

        for category in serializer.validated_data:
            position_dict[category["id"]] = category["position"]
            ids.append(category["id"])

        categories = Category.objects.filter(pk__in=ids)
        existed_ids = [p.id for p in categories]
        wrong_ids = set(ids) - set(existed_ids)
        if wrong_ids:
            raise APIException(_("{} are not existed").format(wrong_ids))

        for c in categories:
            c.position = position_dict[c.id]

        Category.objects.bulk_update(categories, ["position"])

        return Response(data={}, status=status.HTTP_200_OK)

