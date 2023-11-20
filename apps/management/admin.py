# -*- coding: utf-8 -*-
from django.contrib import admin  # noqa
from management.models import (Brand, ChargeOf, Img, MakeupHair, Schedule,
                               Stylist, TimeLocation)

# Register your models here.

admin.site.register(Brand)
admin.site.register(ChargeOf)
admin.site.register(Img)
admin.site.register(Stylist)
admin.site.register(TimeLocation)
admin.site.register(Schedule)
admin.site.register(MakeupHair)
