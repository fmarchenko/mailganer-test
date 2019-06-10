# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from ..models import Event
from ..tasks import send_message_task

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


@receiver(post_save, sender=Event)
def create_event_handler(sender, instance, created, **kwargs):
    if created:
        send_message_task.delay(event_id=instance.pk)
