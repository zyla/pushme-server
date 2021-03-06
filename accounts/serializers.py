from rest_framework import serializers
from django.contrib.auth import authenticate, login
from accounts import models


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is inactive!")
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError("Invalid credentials!")
        else:
            raise serializers.ValidationError("Missing fields!")

class CreateUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = (
            'email',
            'token',
            'password',
        )
        write_only_fields = (
            'password',
        )
        read_only_fields = (
            'token'
        )

    def create(self, attrs, instance=None):
        user = models.User.objects.create_user(**attrs)
        return user

    def get_token(self, obj):
        return str(obj.auth_token)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'email',
        )
