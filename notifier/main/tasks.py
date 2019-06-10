# -*- coding: utf-8 -*-

from __future__ import print_function

import uuid

from celery import shared_task

from .settings import DEFAULT_EMAIL_RECIPIENT
from .models import Event, Template, TemplateLog
from .utils import send_message

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


@shared_task
def send_message_task(event_id):
    event = Event.objects.get(pk=event_id)
    try:
        template = Template.objects.get(shop=event.shop, trigger_type=event.trigger_type)
    except Template.DoesNotExist:
        raise Exception('Undefined template for {}: {}'.format(event.shop, event.get_trigger_type_display()))

    telemetry_uuid = uuid.uuid4()
    recipient = event.context.get('recipient', DEFAULT_EMAIL_RECIPIENT)
    body = template.get_body(context=event.context, telemetry_uuid=telemetry_uuid)
    subject = template.get_subject(context=event.context)
    content_type = template.get_content_type_display()

    log = TemplateLog(template=template, subject=subject, body=body, opening_uuid=telemetry_uuid)
    try:
        send_message(recipient=recipient, body=body, subject=subject, content_type=content_type)
    except Exception as e:
        log.traceback = str(e)
        raise e
    finally:
        log.save()

