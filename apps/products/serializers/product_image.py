from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ProductImageWriteSerializer(serializers.Serializer):
    base64 = serializers.CharField(required=True)
    file_name = serializers.CharField(required=True)

    def validate_file_name(self, file_name):
        extensions = ['.png', '.jpg', '.jpeg', '.svg', '.gif']
        if '.' not in file_name:
            raise serializers.ValidationError(_("File must have the extension"))
        if not file_name.lower().endswith(tuple(extensions)):
            raise serializers.ValidationError(_("File extension `{file_name}` is not allowed. Allowed extensions are: {extensions}").format(file_name=file_name.split('.')[-1], extensions=",".join(extensions)))
        return file_name


class ProductImageReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    file_name = serializers.CharField(read_only=True)
    full_path = serializers.FileField(read_only=True, source="path")
    path = serializers.CharField(read_only=True, source="path.url")
    position = serializers.IntegerField(read_only=True)
    size = serializers.IntegerField(read_only=True)
