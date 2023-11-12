# -*- coding: utf-8 -*-
import base64

import django.contrib.auth.password_validation as validators
from auth_user.api import schemas
from auth_user.api.serializers import (CustomJWTSerializer,
                                       CustomTokenRefreshSerializer,
                                       RegisterSerializer, RoleListSerializer,
                                       UserSerializer, UserUpdateSerializer)
from auth_user.models import Role, User
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from django.core.files.base import ContentFile
from django.db import transaction as trans
from django.http.response import Http404
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from core.utils.api_req import parse_pydantic_obj  # noqa
from core.utils.api_resp import ErrorResponseException, success_api_resp
from core.utils.services import object_to_dict


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            return success_api_resp(data=RegisterSerializer(instance).data)

        raise ErrorResponseException(error=serializer.errors)


@swagger_auto_schema(
    method='post',
    request_body=schemas.UserCreateSchemas,
)
@api_view(('POST',))
@permission_classes([])
@csrf_exempt
def create_user(request):
    # rdata = parse_pydantic_obj(schemas.UserCreateSchemas, request.data)
    serializer = schemas.UserCreateSchemas(data=request.data, context={'request': request})

    if serializer.is_valid():
        rdata = serializer.data
    else:
        errors = serializer.errors
        raise ErrorResponseException(error=errors)

    def validate_password(password):  # noqa
        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password)
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return password

    try:
        role = Role.objects.get(id=rdata['role_id'])

        if User.objects.filter(username=rdata['username']).exists():
            raise serializers.ValidationError({"username": "User name already exists"})

        image_data = request.data.get('avatar')
        if not image_data:
            raise ErrorResponseException(error="missing avatar")
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'avatar.{ext}')

        with trans.atomic():
            user = User.objects.create(
                username=rdata['username'],
                fullname=rdata['fullname'],
                avatar=image_data,
                role=role
            )
            user.set_password(rdata['password'])
            user.is_staff = True
            user.save()

        data = object_to_dict(user)
        data.pop("password")

        data["role"] = {
            "id": role.id,
            "name": role.name
        }

        return success_api_resp(data=data)

    except Exception as e:
        raise ErrorResponseException(error=str(e))


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                validate_data = serializer.validated_data
                password = validate_data.get("password")
                if password:
                    validate_data['password'] = make_password(password)

                serializer.save()
                user = User.objects.get(id=serializer.data["id"])

                image_data = request.data.get('avatar')
                if image_data:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    image_data = ContentFile(base64.b64decode(imgstr), name=f'avatar.{ext}')
                    user.avatar = image_data
                    user.save()

                data = object_to_dict(user)
                data.pop("password")

                data["role"] = {
                    "id": user.role.id,
                    "name": user.role.name
                }

                return success_api_resp(data=data)
            else:
                raise ErrorResponseException(error=serializer.errors)
        except Http404 as e:
            raise ErrorResponseException(error=str(e))


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_api_resp(data=[])

        except Http404 as e:
            raise ErrorResponseException(error=str(e))


class RoleList(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class RoleCreate(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class RoleDetail(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class RoleUpdate(generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_api_resp(data=serializer.data)
            else:
                raise ErrorResponseException(error=serializer.errors)
        except Http404 as e:
            raise ErrorResponseException(error=str(e))


class RoleDelete(generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_api_resp(data=[])

        except Http404 as e:
            raise ErrorResponseException(error=str(e))
