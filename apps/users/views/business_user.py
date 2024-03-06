from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from apps.users.filters import BusinessUserFilterSet
from apps.users.models import BusinessUser, RoleName
from apps.users.serializers import (
    BusinessUserSerializer,
    BusinessUserReadOnlySerializer,
)
from core.mixins import GetSerializerClassMixin
from core.permissions import (
    BusinessUserPermission,
)
# from ..tasks import my_mail


class BusinessUserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = BusinessUser.objects.all()
    serializer_class = BusinessUserSerializer
    serializer_action_classes = {
        "list": BusinessUserReadOnlySerializer,
        "retrieve": BusinessUserReadOnlySerializer,
    }
    filterset_class = BusinessUserFilterSet
    
    def get_queryset(self):
        query = super(BusinessUserViewSet, self).get_queryset()
        user = self.request.user
        # filter using branch for none all_branches permission user
        if not user.is_superuser:
            if not user.branch:
                raise APIException(_("User {user} does not have branch").format(user=user))
            query = query.filter(branch=user.branch).filter(is_block=False)

        return query
    
    @action(
        methods=["GET"],
        detail=False,
        url_path="me",
        url_name="me",
        # filterset_class=None,
        permission_classes=[IsAuthenticated, BusinessUserPermission],
        pagination_class=None,
    )
    
    def me(self, request, *args, **kwargs):
        user = request.user
        # my_mail.apply_async()

        serializer = self.serializer_action_classes.get("retrieve")(
            user.businessuser_set.first()
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)