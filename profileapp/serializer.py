from rest_framework import serializers
from .models import User
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^[A-Za-z]+$', "First name must contain only alphabets")]
    )

    last_name = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^[A-Za-z]+$', "Last name must contain only alphabets")]
    )

    phone = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^\d{10}$', "Phone number must be 10 digits")]
    )

    password = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True
    )

    class Meta:
        model = User
        fields = '__all__'

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
