from rest_framework import serializers
from perfdemo.demo.models import Maker, Widget, Order


class MakerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maker
        fields = ('id', 'name', 'description')


class WidgetSerializer(serializers.ModelSerializer):
    maker = MakerSerializer(many=False, read_only=True)

    class Meta:
        model = Widget
        fields = ('id', 'name', 'description', 'cost', 'created_date', 'maker')


class OrderSerializer(serializers.ModelSerializer):
    widget = WidgetSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'widget', 'order_date')
