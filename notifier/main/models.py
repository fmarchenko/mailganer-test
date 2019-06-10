# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe

from .settings import TELEMETRY_HOST
from .utils import render_template_from_string
from .validators import validate_template, validate_html, validate_template_file

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


@python_2_unicode_compatible
class Shop(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.slug)


class Event(models.Model):
    class TriggerType(object):
        NEW_ORDER = 1
        FORGOTTEN_CART = 2
        FORGOTTEN_SHOP = 3

        CHOICES = (
            (NEW_ORDER, 'new order'),
            (FORGOTTEN_CART, 'forgotten cart'),
            (FORGOTTEN_SHOP, 'forgotten shop')
        )

    shop = models.ForeignKey(Shop, related_name='events')
    trigger_type = models.PositiveSmallIntegerField(choices=TriggerType.CHOICES)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    context = JSONField(default={})


@python_2_unicode_compatible
class Template(models.Model):
    class ContentType(object):
        CONTENT_TYPE_TEXT = 1
        CONTENT_TYPE_HTML = 2

        CHOICES = (
            (CONTENT_TYPE_TEXT, 'plain'),
            (CONTENT_TYPE_HTML, 'html')
        )

    shop = models.ForeignKey(Shop, related_name='templates')
    trigger_type = models.PositiveSmallIntegerField(choices=Event.TriggerType.CHOICES)
    active = models.BooleanField(default=True)
    content_type = models.PositiveSmallIntegerField(
        choices=ContentType.CHOICES, default=ContentType.CONTENT_TYPE_HTML
    )
    subject = models.CharField(validators=[validate_template], max_length=255)
    body = models.TextField(blank=True, null=True, validators=[validate_template, validate_html])
    body_template_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_template_file])

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return '{}: {}'.format(self.shop, self.get_trigger_type_display())

    @mark_safe
    def get_body(self, context, telemetry_uuid=None):
        body = ''
        telemetry = ''

        if self.content_type == self.ContentType.CONTENT_TYPE_HTML:
            telemetry = '<img src="//{}{}" alt="Telemetry" />'.format(
                TELEMETRY_HOST, reverse('telemetry', args=(telemetry_uuid or uuid.uuid4(),)))

        if self.body_template_name:
            body = render_to_string(self.body_template_name, context)
        body = render_template_from_string(self.body, context)

        body = '\n'.join((telemetry, body))

        return body

    def get_subject(self, context):
        return render_template_from_string(self.subject, context)

    def clean(self):
        if not self.body and not self.body_template_name:
            raise ValidationError({'body': 'One of fields body or body_template_name must be filled',
                                   'body_template_name': 'One of fields body or body_template_name must be filled'})


@python_2_unicode_compatible
class TemplateLog(models.Model):
    opening_uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    opening_counter = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='logs')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    traceback = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = 'Logs'
        verbose_name_plural = 'Logs'
        ordering = ['-create_at']

    def __str__(self):
        return '{}: {}'.format(self.template, self.create_at)

    def is_success(self):
        return self.traceback is None

    is_success.admin_order_field = 'traceback'
    is_success.boolean = True
    is_success.short_description = 'Success'
