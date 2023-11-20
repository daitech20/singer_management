# -*- coding: utf-8 -*-
from django.urls import path
from management.api import views

app_name = 'management'
urlpatterns = [
    path('create-brand', views.BrandCreate.as_view(), name='create_brand'),
    path('list-brand', views.BrandList.as_view(), name='list_brand'),
    path('get-brand/<int:id>', views.BrandDetail.as_view(), name='get_brand'),
    path('update-brand/<int:id>', views.BrandUpdate.as_view(), name='update_brand'),
    path('delete-brand/<int:id>', views.BrandDelete.as_view(), name='delete_brand'),
    path('create-charge_of', views.ChargeOfCreate.as_view(), name='create_charge_of'),
    path('list-charge_of', views.ChargeOfList.as_view(), name='list_charge_of'),
    path('get-charge_of/<int:id>', views.ChargeOfDetail.as_view(), name='get_charge_of'),
    path('update-charge_of/<int:id>', views.ChargeOfUpdate.as_view(), name='update_charge_of'),
    path('delete-charge_of/<int:id>', views.ChargeOfDelete.as_view(), name='delete_charge_of'),
    path('create-stylist', views.StylelistCreate.as_view(), name='create_stylist'),
    path('list-stylist', views.StylelistList.as_view(), name='list_stylist'),
    path('get-stylist/<int:id>', views.StylelistDetail.as_view(), name='get_stylist'),
    path('update-stylist/<int:id>', views.StylistUpdate.as_view(), name='update_stylist'),
    path('delete-stylist/<int:id>', views.StylistDelete.as_view(), name='delete_stylist'),
    path('create-makeup_hair', views.MakeupHairCreate.as_view(), name='create_makeup_hair'),
    path('list-makeup_hair', views.MakeupHairList.as_view(), name='list_makeup_hair'),
    path('get-makeup_hair/<int:id>', views.MakeupHairDetail.as_view(), name='get_makeup_hair'),
    path('update-makeup_hair/<int:id>', views.MakeupHairUpdate.as_view(), name='update_makeup_hair'),
    path('delete-makeup_hair/<int:id>', views.MakeupHairDelete.as_view(), name='delete_makeup_hair'),
    path('create-time_location', views.TimeLocationCreate.as_view(), name='create_time_location'),
    path('list-time_location', views.TimeLocationList.as_view(), name='list_time_location'),
    path('get-time_location/<int:id>', views.TimeLocationDetail.as_view(), name='get_time_location'),
    path('update-time_location/<int:id>', views.TimeLocationUpdate.as_view(), name='update_time_location'),
    path('delete-time_location/<int:id>', views.TimeLocationDelete.as_view(), name='delete_time_location'),
    path('create-schedule', views.ScheduleCreate.as_view(), name='create_schedule'),
    path('list-schedule', views.ScheduleListView.as_view(), name='list_schedule'),
]
