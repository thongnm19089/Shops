from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_superuser']
    
    def validate_password(self, password):
        errors = None
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return password
    

    def validate_is_block(self, is_block):
        try:
            user = self.context["request"].user
        except KeyError:
            user = self.context.get('user')
        if user.is_block == is_block:
            return user.is_block
        if not user.is_superuser:
            raise serializers.ValidationError(_('You do not have permission to block user'))
        if self.instance and self.instance.id == user.id:
            raise serializers.ValidationError(_('Cannot block yourself'))
        if self.instance and self.instance.is_superuser and is_block:
            raise serializers.ValidationError(_('Cannot block root user'))
        return is_block
    
    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                if attr == "password":
                    instance.set_password(value)
                else:
                    setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError(
                _("New password must be different from old password")
            )

        try:
            validators.validate_password(password=data["new_password"])
        except Exception as e:
            raise serializers.ValidationError(e)

        return data
