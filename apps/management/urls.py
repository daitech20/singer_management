# -*- coding: utf-8 -*-
from django.urls import include, path

app_name = 'management'
urlpatterns = [
    path('api/v1/', include('apps.management.api')),
]
