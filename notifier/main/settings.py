# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.conf import settings

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


DEFAULT_EMAIL_RECIPIENT = getattr(settings, 'DEFAULT_EMAIL_RECIPIENT', 'dummy@example.com')
TELEMETRY_HOST = getattr(settings, 'TELEMETRY_HOST', 'example.com')
