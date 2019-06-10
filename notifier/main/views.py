# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import logging

from django.db.models.expressions import F
from django.http.response import HttpResponse
from django.views.decorators.cache import cache_control
from django.views.generic import View

from .models import TemplateLog

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"

logger = logging.getLogger(__name__)


class TelemetryView(View):
    @cache_control(must_revalidate=True, max_age=60)
    def get(self, request, telemetry_uuid):
        try:
            TemplateLog.objects.filter(opening_uuid=telemetry_uuid).update(opening_counter=F('opening_counter') + 1)
        except Exception as e:
            logger.warning('[Telemetry] {}'.format(e))
        pixel_image = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        return HttpResponse(pixel_image, content_type='image/gif')
