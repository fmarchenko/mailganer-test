# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .admin_filters import TemplateDateFieldListFilter
from .models import Template, TemplateLog, Shop

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    prepopulated_fields = {'slug': ('name',)}


class TemplateLogInline(admin.TabularInline):
    model = TemplateLog
    extra = 0
    readonly_fields = ('is_success', 'create_at', 'template', 'subject', 'body', 'opening_counter', 'traceback')

    def get_queryset(self, request):
        return super(TemplateLogInline, self).get_queryset(request)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('active', 'shop', 'trigger_type', 'subject', 'total_opening')
    list_display_links = ('shop',)
    inlines = [TemplateLogInline]
    list_filter = ('shop', 'trigger_type', ('logs__create_at', TemplateDateFieldListFilter))

    def total_opening(self, obj):
        return obj.total_opening
    total_opening.admin_order_field = 'total_opening'


@admin.register(TemplateLog)
class TemplateLogAdmin(admin.ModelAdmin):
    readonly_fields = ('opening_counter', 'is_success', 'create_at', 'template', 'subject', 'body', 'traceback')
    list_display = ('is_success', 'template', 'create_at')
    list_display_links = ('template',)
    list_select_related = ('template',)
    list_filter = ('template',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
