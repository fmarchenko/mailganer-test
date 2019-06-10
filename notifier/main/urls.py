# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.conf.urls import url
from rest_framework.generics import CreateAPIView

from .serializers import EventSerializer
from .views import TelemetryView

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"

urlpatterns = [
    url(r'^events/', CreateAPIView.as_view(serializer_class=EventSerializer), name='create-event'),
    url(r'^telemetry/(?P<telemetry_uuid>.+).gif$', TelemetryView.as_view(), name='telemetry')
]
