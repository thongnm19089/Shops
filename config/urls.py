"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

swagger_info = openapi.Info(
    title="Shop API",
    default_version="v1",
    description="""Shop project.""",
    contact=openapi.Contact(email="minh@gmail.com"),
    license=openapi.License(name="Private")
)

schema_view = get_schema_view(
    info=swagger_info,
    public=True,
    # authentication_classes=[rest_framework.authentication.SessionAuthentication],
    permission_classes=[permissions.AllowAny],
)

api_router = SimpleRouter(trailing_slash=False)

from apps.shops.views import (
    ShopViewSet,
    BranchViewSet,
    PrinterViewSet,
)

from apps.auths.views import (
    CustomerRegisterView,
    BusinessLoginView,
    CustomerLoginView,
    CustomerChangePasswordView,
    LogoutView,
)

from apps.users.views import (
    BusinessUserViewSet,
    DeviceView,
)
from apps.customers.views import (
    CustomerViewSet,
)
from apps.products.views import (
    BrandViewSet,
    CategoryViewSet,
    ProductViewSet,
    InventoryViewSet,
    InventoryHistoryViewSet,
)

api_router.register('shops', ShopViewSet, basename='shops')
api_router.register('branches', BranchViewSet, basename='branches')
api_router.register('business_users', BusinessUserViewSet, basename='business_users')
api_router.register('brands', BrandViewSet, basename='brands')
api_router.register('categories', CategoryViewSet, basename='categories')
api_router.register('products', ProductViewSet, basename='products')
api_router.register('customers', CustomerViewSet, basename='customers')
api_router.register('inventories', InventoryViewSet, basename="inventories")
api_router.register('inventory_histories', InventoryHistoryViewSet, basename="inventory_histories")
api_router.register('printers', PrinterViewSet, basename='printers')

from apps.auths.views import index, send, showFirebaseJS
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v1/', include(api_router.urls)),
    path(r'api/v1/business/login', BusinessLoginView.as_view()),
    path(r'api/v1/customer/register', CustomerRegisterView.as_view()),
    path(r'api/v1/customer/login', CustomerLoginView.as_view()),
    path(r'api/v1/logout', LogoutView.as_view()),
    path(r'api/v1/customer/change-password', CustomerChangePasswordView.as_view()),
    path(r'api/v1/devices', DeviceView.as_view()),
    path(r'index', index),
    path(r'send', send),
    path(r'firebase-messaging-sw.js', showFirebaseJS)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.extend([
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
])
