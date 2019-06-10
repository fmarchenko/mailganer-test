# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os

from celery import Celery

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notifier.settings")

app = Celery('notifier')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
