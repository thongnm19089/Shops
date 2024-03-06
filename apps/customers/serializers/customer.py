from rest_framework import serializers

from apps.customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ["user", "title"]
        read_only_fields = ["code"]
        extra_kwargs = {
            "ascii_name": {"required": False},
            "branch": {"required": False},
        }
    
    def validate_email(self, email):
        user = self.context["request"].user
        if self.instance and self.instance.email == email:
            return email
        if not user.is_superuser and email and Customer.objects.filter(email=email).exists():
            msg = _('This email {email} is already existed').format(email=email)
            raise serializers.ValidationError(msg)
        return email

    def validate_phone(self, phone):
        user = self.context["request"].user
        if self.instance and self.instance.phone == phone:
            return phone
        if not user.is_superuser and phone and Customer.objects.filter(phone=phone).exists():
            msg = _('This phone {phone} is already existed').format(phone=phone)
            raise serializers.ValidationError(msg)
        return phone


class CustomerReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    gender = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    district = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    day_of_birth = serializers.IntegerField(read_only=True)
    month_of_birth = serializers.IntegerField(read_only=True)
    year_of_birth = serializers.IntegerField(read_only=True)
    avatar_url = serializers.FileField(read_only=True)
    facebook = serializers.CharField(read_only=True)
    career = serializers.UUIDField(read_only=True, source='career_id')
    branches = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    created_at = serializers.DateTimeField(read_only=True)
    note = serializers.CharField(read_only=True)


class CustomerProfileSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    day_of_birth = serializers.CharField(required=False)
    month_of_birth = serializers.CharField(required=False)
    year_of_birth = serializers.CharField(required=False)
    avatar_url = serializers.FileField(required=False)
    is_block = serializers.BooleanField(required=False)
    role = serializers.UUIDField(required=False)
    shift = serializers.UUIDField(required=False)
    # user = serializers.UUIDField(required=False)
    
    
class CustomerEditProfileSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    day_of_birth = serializers.CharField(required=False)
    month_of_birth = serializers.CharField(required=False)
    year_of_birth = serializers.CharField(required=False)
    avatar_url = serializers.FileField(required=False)
