# -*- coding: utf-8 -*-
# Create your models here.
# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.utils.django_base_models import BaseModel


class Role(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles", null=True, blank=False)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    fullname = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.username
