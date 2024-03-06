import logging

from django.db import transaction
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import UserRolePermission
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound, ParseError

from apps.users.models import User, Role, RoleName, Token
from apps.customers.models import Customer
from apps.users.serializers import ChangePasswordSerializer
from apps.customers.serializers import CustomerReadOnlySerializer

from .serializers import (
    CustomerRegisterSerializer,
    BusinessLoginSerializer,
    TokenSerializer,
    UserLogoutSerializer,
)
import requests
import json
from django.shortcuts import render
# from core.firebase import Firebase

logger = logging.getLogger(__name__)
from django.http import HttpResponse
from core.firebase import sendPush

from core.notification import (
    get_notification_config,
    FCM_CHANNEL,
    get_notification_service,
)
import os
from apps.notifications.tasks import process_send_notification
from apps.notifications.models import Notification

def index(request):
    return render(request, 'index.html', context={})

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js");' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyDk-6BrlcSSWDyPr_1rcitip3IIjdBuGZU",' \
         '        authDomain: "storage-43adb.firebaseapp.com",' \
         '        projectId: "storage-43adb",' \
         '        storageBucket: "storage-43adb.appspot.com",' \
         '        messagingSenderId: "1061053949926",' \
         '        appId: "1:1061053949926:web:291940cbdfcd2030a75827",' \
         '        measurementId: "G-K4LN3K4YTM"' \
         '};' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'
         
    return HttpResponse(data, content_type="text/javascript")

def send(request):
    # C1
    fcm_api = "AAAA9wu-Z-Y:APA91bEig38f4VJx2A1US9yVjgUBGahfqktgwOk88mMuu-OPkNry0-X0w1f1bOQYUS_glm6bcHtYJAyjFpCd1NFBNZSzrLud249w0_601fvLzjQpj2jGd1oqDS34nnXPdBG2-mGyod9g"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "key="+fcm_api
    } 
    
    payload = {
        "to": "eZW2dRWoPhvrPFxhb2mqMX:APA91bHJief5sNh9cORi2WV77GK0CdQBkUnxmV6rW5PNViWHS9ilswBijSVg6z-Ch-LNKF_mUlwRAo_hOb3vM-8YFSTW8YvJD8CoTw03I6rT3pEyYjpzvqJiORa6vW9riu6HvWlUDkWV",
        "notification": {
            "body": "ssssss",
            "title": "hihi",
            "icon": "https://kenh14cdn.com/203336854389633024/2021/3/7/2-16150665819811124794903.jpg",
            "click_action": "https://youtube.com",
        }
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    # C2
    # sendPush(
    #     title="s",
    #     msg="ss",
    #     registration_token=["fevEll88t9o_Da1qH0tI6M:APA91bHpr3IRf-As5-RvGV2--duXJT09oSJpNo2gzQ3ALKWB8yOkfVlPbONx2NewZxueCVRk08w2bd1cxLegMcPSnBE73D_2vvicQvWnl_kJzoCGx0JAHNGy7jZp1c17svAaKIJrakXq","cLRYzFru1RDaZ3Jp3gBQbk:APA91bF75PghPgOb2WbHMh7QtBWF02g0TtqqD-l5c4uePrWUFAvXDNaGEdhSCaMYliPUmadWiiphJzfGPeRJaa-85njfBaJHd9jEKjMFYc33K_l745SNLVxp_Ez5j93tvkmI28ualk3Q"],
    #     dataObject={
    #         'icon': 'https://kenh14cdn.com/203336854389633024/2021/3/7/2-16150665819811124794903.jpg',
    #         'click_action': 'https://youtube.com'
    #     }
    # )
    
    # Test
    # notifications1 = Notification.objects.first()

    # notifications = [{
    #     "notifications": str(notifications1.id)
    # }]
    # process_send_notification(FCM_CHANNEL, notifications)

    return HttpResponse("send")

class CustomerRegisterView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Customer Register",
        request_body=CustomerRegisterSerializer,
        responses={200: CustomerRegisterSerializer()},
    )
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        name = serializer.validated_data.get("name")
        phone = serializer.validated_data.get("phone")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
    
        with transaction.atomic():
            role = Role.objects.get(name=RoleName.CUSTOMER.value)
            user = User.objects.create(
                username=username,
                is_active=True,
                role=role,
            )
            user.set_password(password)
            user.save()
            Customer.objects.create(
                name=name,
                phone=phone,
                email=email,
                user=user,
            )
            # Firebase().create_user(user)

            # TODO: Create active code and send to user
            serializer.validated_data.pop("password")
            serializer.validated_data["user_id"] = user.id
            return Response(
                data=serializer.validated_data, status=status.HTTP_201_CREATED
            )


class CustomerLoginView(views.APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Business Login",
        request_body=BusinessLoginSerializer,
        responses={200: TokenSerializer()},
    )
    def post(self, request):
        serializer = BusinessLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        try:
            user = authenticate(username=username, password=password)
        except User.MultipleObjectsReturned:
            raise APIException(
                _("User with username {username} belongs to multi shops").format(
                    username=username
                ),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except exceptions.NotFound:
            raise APIException(
                _("User or password is wrong"),
                status.HTTP_404_NOT_FOUND,
            )
        except:
            raise APIException(_("Invalid token"), status.HTTP_400_BAD_REQUEST)
        if not user or user.role.name != RoleName.CUSTOMER.value:
            raise APIException(
                _("User with username {username} not found").format(username=username),
                status.HTTP_404_NOT_FOUND,
            )
        if user.is_block:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not user.is_active:
            raise APIException(
                _("User with username {username} has been blocked").format(username=user.username),
                status.HTTP_403_FORBIDDEN,
            )
        token = create_token(user.id, serializer.validated_data.get('device_name'))
        data = {"token": token}
        return Response(data=data, status=status.HTTP_200_OK)


def create_token(user_id, device_name):
    try:
        token = Token.objects.create(
            user_id=user_id,
            device_name=device_name,
        )
    except Exception as e:
        logger.info(f"error on login: {e}")
        raise APIException(_("Cannot create token"), status.HTTP_500_INTERNAL_SERVER_ERROR)
    return token.key


class BusinessLoginView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Business Login",
        request_body=BusinessLoginSerializer,
        responses={200: TokenSerializer()},
    )
    def post(self, request):
        serializer = BusinessLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        try:
            user = authenticate(username=username, password=password)
        except User.MultipleObjectsReturned:
            raise APIException(
                _("User with username {username} belongs to multi shops").format(
                    username=username
                ),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except exceptions.NotFound:
            raise APIException(
                _("User or password is wrong"),
                status.HTTP_404_NOT_FOUND,
            )
        except:
            raise APIException(_("Invalid token"), status.HTTP_400_BAD_REQUEST)
        if not user or user.role.name == RoleName.CUSTOMER.value:
            raise APIException(
                _("User with username {username} not found").format(username=username),
                status.HTTP_404_NOT_FOUND,
            )
        if user.is_block:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not user.is_active:
            raise APIException(
                _("User with username {username} has been blocked").format(username=user.username),
                status.HTTP_403_FORBIDDEN,
            )
        token = create_token(user.id, serializer.validated_data.get('device_name'))
        data = {"token": token}
        return Response(data=data, status=status.HTTP_200_OK)


class CustomerChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change customer's password",
        request_body=ChangePasswordSerializer,
        responses={200: CustomerReadOnlySerializer()},
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            raise APIException(_("Old password is wrong."))
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        Token.objects.filter(user=user).delete()
        serializer = CustomerReadOnlySerializer(user.customer_set.first())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=UserLogoutSerializer,
        responses={200: None},
    )
    def post(self, request):
        user = self.request.user
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('is_logout_all'):
            Token.objects.filter(user=user).delete()
        else:
            Token.objects.filter(user=user, key=str(self.request.auth)).delete()
        return Response(data={}, status=status.HTTP_200_OK)
