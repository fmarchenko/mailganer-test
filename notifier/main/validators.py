# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import lxml.etree

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.template.exceptions import TemplateSyntaxError, TemplateDoesNotExist
from .utils import render_template_from_string

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Jun 10, 2019"


def validate_template(value):
    try:
        render_template_from_string(value)
    except (TemplateSyntaxError, TypeError):
        raise ValidationError('Template syntax error')


def validate_template_file(template_name):
    try:
        validate_html(render_to_string(template_name))
    except (TemplateSyntaxError, TypeError):
        raise ValidationError('Template syntax error')
    except TemplateDoesNotExist:
        raise ValidationError('Template does not exist')


def validate_html(value):
    parser = lxml.etree.HTMLParser(recover=False)
    try:
        lxml.etree.parse(StringIO(value), parser)
    except lxml.etree.XMLSyntaxError:
        raise ValidationError('Html syntax error')

