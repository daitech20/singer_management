# -*- coding: utf-8 -*-
from auth_user.api import views
from django.urls import path

app_name = 'auth_user'
urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('create-user', views.create_user, name='create_user'),
    path('list-user', views.UserList.as_view(), name="list_user"),
    path('get-user/<int:id>', views.UserDetail.as_view(), name='get_user'),
    path('list-role', views.RoleList.as_view(), name='list_role'),
    path('get-role/<int:id>', views.RoleDetail.as_view(), name='get_role'),
    path('update-role/<int:id>', views.RoleUpdate.as_view(), name='update_role'),
    path('delete-role/<int:id>', views.RoleDelete.as_view(), name='delete_role'),
    path('create-role', views.RoleCreate.as_view(), name='create_role'),
    path('update-user/<int:id>', views.UserUpdate.as_view(), name='update_user'),
    path('delete-user/<int:id>', views.UserDelete.as_view(), name='delete_user'),
]
