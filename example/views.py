# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from base.view_utils import BaseMixin


class SettingsView(BaseMixin, TemplateView):

    template_name = 'settings/home.html'
