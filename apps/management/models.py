# -*- coding: utf-8 -*-
from auth_user.models import User
from django.db import models

from core.utils.django_base_models import BaseModel

# Create your models here.


class TimeLocation(BaseModel):
    make_up_time = models.DateTimeField()
    leave_time = models.DateTimeField()
    show_time = models.DateTimeField()
    show_date = models.DateField()
    show_localtion = models.CharField(max_length=255)
    agency_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=11)


class ChargeOf(BaseModel):
    name = models.CharField(max_length=50)


class Brand(BaseModel):
    name = models.CharField(max_length=50, unique=True)


class Img(BaseModel):
    value = models.ImageField(upload_to='img')


class Stylist(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    images = models.ManyToManyField(Img, blank=True)


class MakeupHair(BaseModel):
    make_up = models.CharField(max_length=50)
    make_hair = models.CharField(max_length=50)
    images = models.ManyToManyField(Img, blank=True)


class Schedule(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_users')
    time_localtion_id = models.ForeignKey(TimeLocation, on_delete=models.CASCADE,
                                          related_name='schedule_time_locations')
    makeup_hair_id = models.ForeignKey(MakeupHair, on_delete=models.CASCADE, related_name='chedule_makeup_hairs')
    stylist_id = models.ForeignKey(Stylist, on_delete=models.CASCADE, related_name='schedule_stylists')
    charge_of_id = models.ForeignKey(ChargeOf, on_delete=models.CASCADE, related_name='schedule_charge_ofs')
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='schedule_brands')


class Device(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_users')
    push_token = models.CharField(max_length=255)
