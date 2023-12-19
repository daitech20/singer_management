# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from management.models import Schedule
from management.tasks import notify_singer

from singer_management.celery import app

# @receiver(pre_save, sender=Schedule)
# def schedule_pre_save(sender, instance, **kwargs):
#     if instance.pk:
#         old_instance = Schedule.objects.get(pk=instance.pk)
#         # if old_instance.time_localtion_id.show_time != instance.time_localtion_id.show_time:
#         #     if old_instance.scheduled_task_id:
#         #         app.control.revoke(old_instance.scheduled_task_id)

#         #     task = notify_singer.apply_async(
#         #         args=[instance.id], eta=instance.time_localtion_id.show_time - timedelta(hours=4))
#         #     instance.scheduled_task_id = task.id
#         if old_instance.scheduled_task_id:
#             app.control.revoke(old_instance.scheduled_task_id)

#         combined_datetime = datetime.combine(instance.time_localtion_id.show_date, instance.time_localtion_id.show_time) # noqa

#         task = notify_singer.apply_async(
#             args=[instance.id], eta=combined_datetime - timedelta(hours=4))
#         instance.scheduled_task_id = task.id


@receiver(post_save, sender=Schedule)
def schedule_post_save(sender, instance, created, **kwargs):
    if not created:
        if instance.scheduled_task_id:
            app.control.revoke(instance.scheduled_task_id)

    combined_datetime = datetime.combine(instance.time_localtion_id.show_date, instance.time_localtion_id.show_time)

    task = notify_singer.apply_async(
        args=[instance.id], eta=timezone.make_aware(combined_datetime, timezone=timezone.get_default_timezone()) - timedelta(hours=4))  # noqa

    post_save.disconnect(schedule_post_save, sender=Schedule)
    instance.scheduled_task_id = task.id
    instance.save(update_fields=['scheduled_task_id'])
    post_save.connect(schedule_post_save, sender=Schedule)
