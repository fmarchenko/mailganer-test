# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from rest_framework import serializers

from .models import Event

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


class EventSerializer(serializers.ModelSerializer):
    context = serializers.JSONField(default={}, initial={})

    class Meta:
        model = Event
        fields = ('shop', 'trigger_type', 'context')
