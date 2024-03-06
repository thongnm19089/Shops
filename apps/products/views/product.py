import os
import shutil
import uuid
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import datetime
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.db.models import Prefetch, QuerySet, F, Q
from apps.products.models import (
    Product,
    ProductImage,
    Variant,
    VariantOption,
)
from apps.products.serializers import (
    ProductSerializer,
    ProductReadOnlySerializer,
    ProductRetrieveSerializer,
)
from apps.products.serializers.product import UpdatePositionSerializer

from core.mixins import GetSerializerClassMixin, GetPermissionClassMixin
from core.permissions import (
    BusinessUserPermission,
)

from django.core.files.storage import FileSystemStorage, default_storage
from core.util import get_size
from core.query_debugger import query_debugger


class ProductViewSet(GetSerializerClassMixin, GetPermissionClassMixin, viewsets.ModelViewSet):
    queryset = Product.objects.select_related('brand', 'category').prefetch_related(
        Prefetch("productimage_set", queryset=ProductImage.objects.all()),
        Prefetch("variantoption_set", queryset=VariantOption.objects.all()),
        Prefetch("variants", queryset=Variant.objects.prefetch_related("productimage_set")),
    )

    serializer_class = ProductSerializer
    serializer_action_classes = {
        "list": ProductReadOnlySerializer,
        "retrieve": ProductRetrieveSerializer,
    }
    permission_classes = [BusinessUserPermission]
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
    }
    
    @query_debugger
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_action_classes.get("retrieve")(self.queryset, many=True)
        return Response(serializer.data)
    
    
    @query_debugger
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)        

        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # product_images = serializer.validated_data.pop('product_images')
        images = serializer.validated_data.pop('images', None)
        with transaction.atomic():
            instance = serializer.save()
            self._create_product_images(instance.id, images)
        
        serializer = self.serializer_action_classes.get("retrieve")(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        product_images = serializer.validated_data.pop('product_images', None)
        product_image_id = serializer.validated_data.pop("product_image_id", None)
        with transaction.atomic():
            old_image = instance.image_url
            product_id = instance.id
            if old_image and serializer.validated_data.get("image_url"):
                destination_path = os.path.join(settings.MEDIA_ROOT, "shops", "product", str(product_id))
                if os.path.isdir(destination_path):
                    os.unlink("media" + "/" + str(old_image))

            instance = serializer.save()
            self._upsert_product_images(instance.id, product_images, product_image_id, True)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
            
        serializer = self.serializer_action_classes.get("retrieve")(instance)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product_id = instance.id
        self.perform_destroy(instance)
        ProductImage.objects.filter(id=product_id).delete()
        destination_path = os.path.join(settings.MEDIA_ROOT, "shops", "product", str(product_id))
        if os.path.isdir(destination_path):
            shutil.rmtree(destination_path)
       
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        query_serializer=UpdatePositionSerializer, responses={200: None,}
    )
    @action(
        methods=["PUT"],
        detail=False,
        url_path="update_position",
        url_name="update_position",
        serializer_class=UpdatePositionSerializer,
    )
    def update_position(self, request, *args, **kwargs):
        serializer = UpdatePositionSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        user = request.user
        ids = []
        position_dict = dict()

        for product in serializer.validated_data:
            position_dict[product["id"]] = product["position"]
            ids.append(product["id"])

        products = Product.objects.filter(pk__in=ids)
        existed_ids = [p.id for p in products]
        wrong_ids = set(ids) - set(existed_ids)
        if wrong_ids:
            raise APIException("{} are not existed".format(wrong_ids))

        for p in products:
            p.position = position_dict[p.id]

        Product.objects.bulk_update(products, ["position"])

        return Response(data={}, status=status.HTTP_200_OK)


    def _create_product_images(self, product_id, images):
        if images is not None:
            pictures = []
            position = 1
            
            for image in images:
                format, imgstr = image["base64"].split(';base64,')
                # ext = format.split('/')[-1]
                file_name = image["file_name"]
                path = ContentFile(base64.b64decode(imgstr), name=file_name)
                picture = ProductImage(
                    file_name = file_name,
                    size = get_size(imgstr),
                    path = path,
                    product_id = product_id,
                    position = position
                )
                pictures.append(picture)
                position = position + 1

            ProductImage.objects.bulk_create(pictures)

