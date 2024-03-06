from django.core import exceptions
from django.contrib.auth import password_validation

from apps.users.models import User
from apps.customers.models import Customer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class CustomerRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    name = serializers.CharField(max_length=50, required=True)
    phone = serializers.CharField(max_length=10, required=True)
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=128, required=True)
    
    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError(
                _("User with username {username} is existed").format(username=username)
            )
        return username
        
    def validate_email(self, email):
        if Customer.objects.filter(email=email):
            raise serializers.ValidationError(
                _('This email {email} is already existed').format(email=email)                
            )
        return email

    def validate_phone(self, phone):
        if Customer.objects.filter(phone=phone):
            raise serializers.ValidationError(
                _("User with phone {phone} is existed").format(phone=phone)
            )
        return phone

    def validate_password(self, password):
        errors = None
        try:
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return password


class BusinessLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)
    device_name = serializers.CharField(max_length=100, required=False)
    

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class ActiveCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    user_id = serializers.UUIDField(required=True)

class UserLogoutSerializer(serializers.Serializer):
    is_logout_all = serializers.BooleanField(required=False)
