# -*- coding: utf-8 -*-
from datetime import date, datetime

from django.db.models.fields.files import ImageFieldFile


def object_to_dict(obj):
    if not obj:
        return None

    object_dict = {}
    for field in obj._meta.fields:
        field_name = field.name
        field_value = getattr(obj, field_name)

        if isinstance(field_value, datetime):
            field_value = field_value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(field_value, date):
            field_value = field_value.strftime('%Y-%m-%d')
        if isinstance(field_value, ImageFieldFile):
            field_value = field_value.url if field_value else None

        if not field_name.startswith('_'):
            object_dict[field_name] = field_value

    return object_dict


def code_to_datetime(timestamp):
    dt_object = datetime.fromtimestamp(int(timestamp))
    return dt_object


def create_email_by_student_id(student_id):
    student_id = student_id.lower()
    email = f'{student_id}@student.ptithcm.edu.vn'

    return email
