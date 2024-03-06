import json

from django.contrib.auth.models import AnonymousUser
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework_extensions.cache.mixins import BaseCacheResponseMixin
from rest_framework import serializers

from core.cache import custom_cache_response


class TenantGetQuerysetMixin:
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


class GetSerializerClassMixin:
    serializer_action_classes = {}

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

class GetPermissionClassMixin:
    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            # return permission_classes depending on action 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

class TenantSerializerMixin:
    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if hasattr(self.context["request"], "user"):
            user = self.context["request"].user
            if not isinstance(user, AnonymousUser) and user.tenant:
                ret["tenant"] = user.tenant
        if hasattr(self.context["request"], "api_key"):
            api_key = self.context["request"].api_key
            if api_key.tenant:
                ret["tenant"] = api_key.tenant
        return ret


class BranchQuerySetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, "user"):
            user = self.request.user
            if user.branch and not user.role.has_branches_permission:
                queryset = queryset.filter(branch_id=user.branch_id)

        return queryset


class ListCustomCacheResponseMixin(BaseCacheResponseMixin):
    @custom_cache_response(key_func='list_cache_key_func', timeout='list_cache_timeout')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RetrieveCustomCacheResponseMixin(BaseCacheResponseMixin):
    @custom_cache_response(key_func='object_cache_key_func', timeout='object_cache_timeout')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CustomCacheResponseMixin(RetrieveCustomCacheResponseMixin,
                               ListCustomCacheResponseMixin):

    def list_cache_key_func(self, view_instance, view_method, request: Request, args, kwargs):
        return ".".join([
            view_instance.basename,
            view_instance.action,
            f"query_{json.dumps(request.query_params)}",
        ])

    def object_cache_key_func(self, view_instance, view_method, request: Request, args, kwargs):
        return ".".join([
            view_instance.basename,
            view_instance.action,
            f"pk_{kwargs['pk']}",
        ])
