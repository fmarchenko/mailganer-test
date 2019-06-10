# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import logging

from django.core.mail import EmailMessage
from django.template import Template, Context

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"

logger = logging.getLogger(__name__)


def render_template_from_string(string, context=None):
    template = Template(string)
    return ''.join(template.render(Context(context)))


def send_message(recipient, body, subject, content_type=None):
    if not isinstance(recipient, (list, tuple)):
        recipient = [recipient]

    message = EmailMessage(subject=subject, body=body, to=recipient)
    if content_type:
        message.content_subtype = content_type
    try:
        message.send()
    except Exception as e:
        logger.error('[Send message] {}'.format(e))
        raise Exception('Send message: {}'.format(e))
    return True
