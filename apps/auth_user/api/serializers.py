# -*- coding: utf-8 -*-
import django.contrib.auth.password_validation as validators  # noqa
from auth_user.models import Role, User
from django.core import exceptions  # noqa
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)

from singer_management.config import sconfigs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include

        avatar_url = None
        if self.user.avatar:
            avatar_url = self.user.avatar.url

        if avatar_url and sconfigs.HOST_LOCAL in avatar_url:
            avatar_url = avatar_url.replace(sconfigs.HOST_LOCAL, sconfigs.HOST_DOMAINT)
        elif avatar_url and sconfigs.HOST_LOCAL not in avatar_url:
            avatar_url = f"{sconfigs.HOST_DOMAINT}{avatar_url}"

        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'fullname': self.user.fullname,
                'is_superuser': self.user.is_superuser,
                'is_staff': self.user.is_staff,
                'avatar': avatar_url,
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
    avatar = Base64ImageField()
    role_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'fullname', 'avatar', 'role_id']

    # def validate(self, attrs):
    #     errors = dict()
    #     try:
    #         validators.validate_password(password=attrs['password'])
    #     except exceptions.ValidationError as e:
    #         errors['password'] = list(e.messages)

    #     if errors:
    #         raise serializers.ValidationError(errors)

    #     return attrs

    def create(self, validated_data):
        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError({"username": "User name already exists"})

        try:
            role = Role.objects.get(id=validated_data['role_id'])
        except Exception as e:
            raise serializers.ValidationError(str(e))

        user = User.objects.create(
            username=validated_data['username'],
            fullname=validated_data['fullname'],
            avatar=validated_data['avatar'],
            role=role
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
        data = super().to_representation(instance)

        avatar = data.get('avatar')

        if avatar and sconfigs.HOST_LOCAL in avatar:
            avatar = avatar.replace(sconfigs.HOST_LOCAL, sconfigs.HOST_DOMAINT)
            data['avatar'] = avatar
        elif avatar and sconfigs.HOST_LOCAL not in avatar:
            data['avatar'] = f"{sconfigs.HOST_DOMAINT}{avatar}"

        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField()
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('id', 'fullname', 'role_id', 'avatar')
