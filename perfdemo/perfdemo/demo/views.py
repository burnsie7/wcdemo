# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic

from perfdemo.demo.models import Maker


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'demo_index'

    def get_queryset(self):
        return Maker.objects.all().order_by('id')
