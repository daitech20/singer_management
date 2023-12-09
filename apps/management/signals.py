# -*- coding: utf-8 -*-
from datetime import timedelta

from celery import current_app
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from management.models import Schedule
from management.tasks import notify_singer


@receiver(pre_save, sender=Schedule)
def schedule_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Schedule.objects.get(pk=instance.pk)
        if old_instance.time_localtion_id.show_time != instance.time_localtion_id.show_time:
            if old_instance.scheduled_task_id:
                current_app.revoke(old_instance.scheduled_task_id)


@receiver(post_save, sender=Schedule)
def schedule_post_save(sender, instance, created, **kwargs):
    if created or (instance.pk and Schedule.objects.get(pk=instance.pk).time_localtion_id.show_time != instance.time_localtion_id.show_time):  # noqa

        task = notify_singer.apply_async(
            args=[instance.id], eta=instance.time_localtion_id.show_time - timedelta(hours=4))

        instance.scheduled_task_id = task.id
        instance.save()
