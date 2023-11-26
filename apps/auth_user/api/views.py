# -*- coding: utf-8 -*-
from auth_user.api.serializers import (CustomJWTSerializer,
                                       CustomTokenRefreshSerializer,
                                       RegisterSerializer, RoleListSerializer,
                                       UserSerializer, UserUpdateSerializer)
from auth_user.models import Role, User
from django.db import IntegrityError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from core.utils.api_req import parse_pydantic_obj  # noqa
from core.utils.api_resp import ErrorResponseException, success_api_resp


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
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

    def perform_update(self, serializer):
        new_password = self.request.data.get('password')
        if new_password:
            user_instance = serializer.instance
            user_instance.set_password(new_password)
            user_instance.save()

        super().perform_update(serializer)

    def update(self, request, *args, **kwargs):
        try:

            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)

                return success_api_resp(data=serializer.data)
            else:

                raise ErrorResponseException(error=serializer.errors)
        except IntegrityError:
            raise ErrorResponseException(error="role_id not exists")
        except Exception as e:
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

        except Exception as e:
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
        except Exception as e:
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

        except Exception as e:
            raise ErrorResponseException(error=str(e))
