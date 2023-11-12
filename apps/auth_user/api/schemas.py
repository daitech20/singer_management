# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.utils.base_schema import CustomBaseModel  # noqa


class UserCreateSchemas(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=50)
    fullname = serializers.CharField(max_length=50)
    role_id = serializers.IntegerField()
    avatar = serializers.FileField()
