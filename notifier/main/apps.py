# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals.handlers  # NOQA