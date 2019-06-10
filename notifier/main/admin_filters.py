# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.contrib.admin.filters import DateFieldListFilter
from django.db.models.aggregates import Sum

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


class TemplateDateFieldListFilter(DateFieldListFilter):
    title = 'send date'

    def queryset(self, request, queryset):
        qs = super(TemplateDateFieldListFilter, self).queryset(request, queryset)\
            .distinct().annotate(total_opening=Sum('logs__opening_counter'))
        return qs
