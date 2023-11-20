# -*- coding: utf-8 -*-
from management.api.serializers import (BrandListSerializer,
                                        ChargeOfListSerializer,
                                        MakeupHairCreateSerializer,
                                        MakeupHairListSerializer,
                                        MakeupHairUpdateSerializer,
                                        ScheduleListParamsSerializer,
                                        ScheduleListSerializer,
                                        ScheduleSerializer,
                                        StylistCreateSerializer,
                                        StylistListSerializer,
                                        StylistUpdateSerializer,
                                        TimeLocationSerializer)
from management.models import (Brand, ChargeOf, MakeupHair, Schedule, Stylist,
                               TimeLocation)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils.api_req import parse_pydantic_obj  # noqa
from core.utils.api_resp import ErrorResponseException, success_api_resp


class BrandCreate(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class BrandDetail(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class BrandUpdate(generics.UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_api_resp(data=serializer.data)
            else:
                raise ErrorResponseException(error=serializer.errors)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class BrandDelete(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_api_resp(data=[])

        except Exception as e:
            raise ErrorResponseException(error=str(e))


class ChargeOfCreate(generics.CreateAPIView):
    queryset = ChargeOf.objects.all()
    serializer_class = ChargeOfListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class ChargeOfList(generics.ListAPIView):
    queryset = ChargeOf.objects.all()
    serializer_class = ChargeOfListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class ChargeOfDetail(generics.RetrieveAPIView):
    queryset = ChargeOf.objects.all()
    serializer_class = ChargeOfListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class ChargeOfUpdate(generics.UpdateAPIView):
    queryset = ChargeOf.objects.all()
    serializer_class = ChargeOfListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_api_resp(data=serializer.data)
            else:
                raise ErrorResponseException(error=serializer.errors)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class ChargeOfDelete(generics.DestroyAPIView):
    queryset = ChargeOf.objects.all()
    serializer_class = ChargeOfListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_api_resp(data=[])

        except Exception as e:
            raise ErrorResponseException(error=str(e))


class StylelistCreate(generics.CreateAPIView):
    queryset = Stylist.objects.all()
    serializer_class = StylistCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class StylelistList(generics.ListAPIView):
    queryset = Stylist.objects.all()
    serializer_class = StylistListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class StylelistDetail(generics.RetrieveAPIView):
    queryset = Stylist.objects.all()
    serializer_class = StylistListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class StylistUpdate(generics.UpdateAPIView):
    queryset = Stylist.objects.all()
    serializer_class = StylistUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class StylistDelete(generics.DestroyAPIView):
    queryset = Stylist.objects.all()
    serializer_class = StylistListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.images.all().delete()
            instance.delete()
            return success_api_resp(data=[])

        except Exception as e:
            raise ErrorResponseException(error=str(e))


class MakeupHairCreate(generics.CreateAPIView):
    queryset = MakeupHair.objects.all()
    serializer_class = MakeupHairCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class MakeupHairList(generics.ListAPIView):
    queryset = MakeupHair.objects.all()
    serializer_class = MakeupHairListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class MakeupHairDetail(generics.RetrieveAPIView):
    queryset = MakeupHair.objects.all()
    serializer_class = MakeupHairListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class MakeupHairUpdate(generics.UpdateAPIView):
    queryset = MakeupHair.objects.all()
    serializer_class = MakeupHairUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class MakeupHairDelete(generics.DestroyAPIView):
    queryset = MakeupHair.objects.all()
    serializer_class = MakeupHairListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.images.all().delete()
            instance.delete()
            return success_api_resp(data=[])

        except Exception as e:
            raise ErrorResponseException(error=str(e))


class TimeLocationCreate(generics.CreateAPIView):
    queryset = TimeLocation.objects.all()
    serializer_class = TimeLocationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class TimeLocationList(generics.ListAPIView):
    queryset = TimeLocation.objects.all()
    serializer_class = TimeLocationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class TimeLocationDetail(generics.RetrieveAPIView):
    queryset = TimeLocation.objects.all()
    serializer_class = TimeLocationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class TimeLocationUpdate(generics.UpdateAPIView):
    queryset = TimeLocation.objects.all()
    serializer_class = TimeLocationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_api_resp(data=serializer.data)
            else:
                raise ErrorResponseException(error=serializer.errors)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


class TimeLocationDelete(generics.DestroyAPIView):
    queryset = TimeLocation.objects.all()
    serializer_class = TimeLocationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_api_resp(data=[])

        except Exception as e:
            raise ErrorResponseException(error=str(e))


class ScheduleCreate(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return success_api_resp(data=serializer.data)


class ScheduleListView(APIView):
    def get_queryset(self, serializer):
        user_id = serializer.validated_data['user_id']
        date = serializer.validated_data['date']
        type_date = serializer.validated_data['type_date']

        queryset = Schedule.objects.none()
        if type_date == 0:
            queryset = Schedule.objects.filter(time_localtion_id__show_date__year=date.year)
        elif type_date == 1:
            queryset = Schedule.objects.filter(time_localtion_id__show_date__month=date.month)
        elif type_date == 2:
            queryset = Schedule.objects.filter(time_localtion_id__show_date__day=date.day)

        if user_id != 0:
            queryset = Schedule.objects.filter(user_id__id=user_id)

        return queryset

    def post(self, request, format=None):
        serializer = ScheduleListParamsSerializer(data=request.data)
        if serializer.is_valid():
            queryset = self.get_queryset(serializer)
            serializer = ScheduleListSerializer(queryset, many=True)

            return success_api_resp(data=serializer.data)
        else:
            raise ErrorResponseException(error=serializer.errors)
