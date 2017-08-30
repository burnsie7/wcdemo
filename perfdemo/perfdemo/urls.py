from django.conf.urls import url
from django.contrib import admin

import perfdemo.demo.api as demo_api

from perfdemo.demo.views import IndexView

urlpatterns = [
    # rest_framework
    url(r'^api/maker/$', demo_api.MakerListView.as_view(), name='maker-list'),
    url(r'^api/maker/create/$', demo_api.MakerCreateView.as_view(), name='maker-create'),
    url(r'^api/maker/(?P<pk>[0-9]+)/$', demo_api.MakerDetailView.as_view(), name='maker-detail'),
    url(r'^api/widget/$', demo_api.WidgetListView.as_view(), name='widget-list'),
    url(r'^api/widget/create/$', demo_api.WidgetCreateView.as_view(), name='widget-create'),
    url(r'^api/widget/(?P<pk>[0-9]+)/$', demo_api.WidgetDetailView.as_view(), name='widget-detail'),
    url(r'^api/order/$', demo_api.OrderListView.as_view(), name='order-list'),
    url(r'^api/order/create/$', demo_api.OrderCreateView.as_view(), name='order-create'),
    url(r'^api/order/(?P<pk>[0-9]+)/$', demo_api.OrderDetailView.as_view(), name='order-detail'),
    url(r'^api/long/$', demo_api.LongQueryView.as_view(), name='long-query'),
    url(r'^api/error/$', demo_api.ThrowErrorView.as_view(), name='throw-error'),

    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
]
