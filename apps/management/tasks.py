# -*- coding: utf-8 -*-
from auth_user.models import Role, User
from celery.utils.log import get_task_logger
from management.models import Schedule
from management.services import send_notify

from singer_management.celery import app

logger = get_task_logger(__name__)


@app.task()
def notify_singer(schedule_id):
    try:
        schedule = Schedule.objects.get(pk=schedule_id)
        user = schedule.user_id
        role = Role.objects.get(name="manager")
        managers = User.objects.filter(role=role)

        expoPushTokens = []

        user_tokens = user.device_users.all()
        for user_token in user_tokens:
            expoPushTokens.append(user_token.push_token)

        for manager in managers:
            for user_token in manager:
                expoPushTokens.append(user_token.push_token)

        for token in expoPushTokens:
            send_notify(token)

    except Exception as e:
        logger.error(str(e))
