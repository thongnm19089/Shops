from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from apps.users.models import User, RoleName
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed, AuthenticationFailed

class UserRolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not isinstance(user, User):
            return False
        if user.is_superuser:
            return True
        if user.is_block:
            raise AuthenticationFailed("USER_BLOCKED")
        if request.method.lower() not in view.action_map:
            raise MethodNotAllowed(_("Method {method} is not allowed on this api. "
                                 "Only {allowed_methods} is allowed!").format(method=request.method,
                                                                              allowed_methods=view.allowed_methods))
        return True

class CustomerUserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not isinstance(user, User):
            return False
        
        return request.user.role.name == RoleName.CUSTOMER.value
    
class BusinessUserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not isinstance(user, User):
            return False
        
        return request.user.role.name != RoleName.CUSTOMER.value
        
        
