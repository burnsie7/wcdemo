import logging

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from perfdemo.demo.models import Maker, Widget, Order
from perfdemo.demo.serializers import MakerSerializer, WidgetSerializer, OrderSerializer
from perfdemo.demo.tasks import create_maker, create_widget, create_order

from datadog import statsd

logger = logging.getLogger(__name__)


class MakerListView(generics.ListAPIView):

    serializer_class = MakerSerializer

    def get_queryset(self):
        stats.increment('api.views', tags=['object:maker', 'view:list'])
        return Maker.objects.all().order_by('-id')


class MakerCreateView(generics.GenericAPIView):

    def post(self, request):
        stats.increment('api.views', tags=['object:maker', 'view:create'])
        create_maker()
        return Response({'Good': 'Making a Maker'}, status=status.HTTP_201_CREATED)


class MakerDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = MakerSerializer

    def get_queryset(self):
        stats.increment('api.views', tags=['object:maker', 'view:detail'])
        maker_id = self.kwargs['pk']
        return Maker.objects.filter(id=maker_id)


class WidgetListView(generics.ListAPIView):

    serializer_class = WidgetSerializer

    def get_queryset(self):
        stats.increment('api.views', tags=['object:widget', 'view:list'])
        return Widget.objects.all().order_by('-id')


class WidgetCreateView(generics.GenericAPIView):

    def post(self, request):
        stats.increment('api.views', tags=['object:widget', 'view:create'])
        create_widget()
        return Response({'Good': 'Making a Widget'}, status=status.HTTP_201_CREATED)


class WidgetDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = WidgetSerializer

    def get_queryset(self):
        stats.increment('api.views', tags=['object:widget', 'view:detail'])
        widget_id = self.kwargs['pk']
        return Widget.objects.filter(id=widget_id)


class OrderListView(generics.ListAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):
        stats.increment('api.views', tags=['object:order', 'view:list'])
        return Order.objects.all().order_by('-id')


class OrderCreateView(generics.GenericAPIView):

    def post(self, request):
        stats.increment('api.views', tags=['object:order', 'view:create'])
        create_order()
        return Response({'Good': 'Making an Order'}, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):
        # TODO: Still returning multiple values for these
        stats.increment('api.views', tags=['object:order', 'view:detail'])
        order_id = self.kwargs['pk']
        return Order.objects.filter(id=order_id)


class LongQueryView(generics.GenericAPIView):

    def get(self, request):
        Order.objects.filter(name__startswith='z'
            ).exclude(name__contains='f'
            ).filter(widget__name__contains='x'
            ).filter(widget__order__name__contains='s')
        return Response({'Good': 'Ran Query'}, status=status.HTTP_200_OK)


class ThrowErrorView(generics.GenericAPIView):

    def get(self, request):
        raise Anything
