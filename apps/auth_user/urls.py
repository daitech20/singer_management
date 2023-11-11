# -*- coding: utf-8 -*-
from django.urls import include, path

app_name = 'auth_user'
urlpatterns = [
    path('api/v1/', include('apps.auth_user.api')),
]
