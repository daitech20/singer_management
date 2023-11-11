# -*- coding: utf-8 -*-
from auth_user.models import Role, User
from django.contrib import admin

# Register your models here.


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'username', )
