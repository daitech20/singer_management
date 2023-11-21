# -*- coding: utf-8 -*-
from auth_user.api.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from management.models import (Brand, ChargeOf, Img, MakeupHair, Schedule,
                               Stylist, TimeLocation)
from rest_framework import serializers

from singer_management.config import sconfigs


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name',)


class ChargeOfListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeOf
        fields = ('id', 'name',)


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ('id', 'value',)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        image_value = data.get('value')

        if image_value and sconfigs.HOST_LOCAL in image_value:
            image_value = image_value.replace(sconfigs.HOST_LOCAL, sconfigs.HOST_DOMAINT)
            data['value'] = image_value
        elif image_value and sconfigs.HOST_LOCAL not in image_value:
            data['avatar'] = f"{sconfigs.HOST_DOMAINT}{image_value}"

        return data


class ImgCreateSerializer(serializers.ModelSerializer):
    value = Base64ImageField(required=False)

    class Meta:
        model = Img
        fields = ('id', 'value',)


class StylistListSerializer(serializers.ModelSerializer):
    images = ImgSerializer(many=True)

    class Meta:
        model = Stylist
        fields = ('id', 'name', 'images')


class StylistCreateSerializer(serializers.ModelSerializer):
    images = ImgCreateSerializer(many=True, required=False)

    class Meta:
        model = Stylist
        fields = ('id', 'name', 'images')

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        stylist = Stylist.objects.create(**validated_data)

        for image_data in images_data:
            img = Img.objects.create(**image_data)
            stylist.images.add(img)

        stylist.save()

        return stylist


class StylistUpdateSerializer(serializers.ModelSerializer):
    images = ImgCreateSerializer(many=True, required=False)

    class Meta:
        model = Stylist
        fields = ('id', 'name', 'images')

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance = super(StylistUpdateSerializer, self).update(instance, validated_data)
        instance.images.clear()
        for image_data in images_data:
            img = Img.objects.create(**image_data)
            instance.images.add(img)

        instance.save()

        return instance


class MakeupHairListSerializer(serializers.ModelSerializer):
    images = ImgSerializer(many=True)

    class Meta:
        model = MakeupHair
        fields = ('id', 'make_up', 'make_hair', 'images')


class MakeupHairCreateSerializer(serializers.ModelSerializer):
    images = ImgCreateSerializer(many=True, required=False)

    class Meta:
        model = MakeupHair
        fields = ('id', 'make_up', 'make_hair', 'images')

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        makeup_hair = MakeupHair.objects.create(**validated_data)

        for image_data in images_data:
            img = Img.objects.create(**image_data)
            makeup_hair.images.add(img)

        makeup_hair.save()

        return makeup_hair


class MakeupHairUpdateSerializer(serializers.ModelSerializer):
    images = ImgCreateSerializer(many=True, required=False)

    class Meta:
        model = MakeupHair
        fields = ('id', 'make_up', 'make_hair', 'images')

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        super(MakeupHairUpdateSerializer, self).update(instance, validated_data)

        instance.images.clear()
        for image_data in images_data:
            img = Img.objects.create(**image_data)
            instance.images.add(img)

        instance.save()

        return instance


class TimeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLocation
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleListSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    time_localtion_id = TimeLocationSerializer()
    makeup_hair_id = MakeupHairListSerializer()
    stylist_id = StylistListSerializer()
    charge_of_id = ChargeOfListSerializer()
    brand_id = BrandListSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleListParamsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.DateField(input_formats=['%d-%m-%Y'])
    type_date = serializers.IntegerField()

    def validate_type_date(self, value):
        if value not in [0, 1, 2]:
            raise serializers.ValidationError("Invalid type_date value.")
        return value
