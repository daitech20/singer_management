# -*- coding: utf-8 -*-
import django.contrib.auth.password_validation as validators
from auth_user.models import Role, User
from django.core import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'fullname': self.user.fullname,
                'is_superuser': self.user.is_superuser,
                'is_staff': self.user.is_staff,
                'avatar': self.user.avatar.url if self.user.avatar else None,
                'role': {
                    'id': self.user.role.id,
                    'name': self.user.role.name
                }
            }
        })
        response_data = {
            'success': 1,
            'data': data
        }

        return response_data


class CustomJWTSerializer(MyTokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        # This is answering the original question, but do whatever you need here.
        # For example in my case I had to check a different model that stores more user info
        # But in the end, you should obtain the username to continue.
        user_obj = User.objects.filter(email=attrs.get("username")).first(
        ) or User.objects.filter(username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        response_data = {
            'success': 1,
            'data': data
        }

        return response_data


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    fullname = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'fullname']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=attrs['password'])
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError({"username": "User name already exists"})

        user = User.objects.create(
            username=validated_data['username'],
            fullname=validated_data['fullname']
        )

        user.set_password(validated_data['password'])
        user.is_staff = True

        user.save()

        return user


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name',)


class UserSerializer(serializers.ModelSerializer):
    role = RoleListSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'is_superuser', 'is_staff', 'role', 'avatar')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['avatar'] = instance.avatar.url if instance.avatar else None

        return representation


class UserUpdateSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        source='role',
        queryset=Role.objects.all(),
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'password', 'fullname', 'role_id', 'avatar')

    def get_image_field(self, obj):
        image_path = obj.avatar.url

        return image_path if image_path else None
