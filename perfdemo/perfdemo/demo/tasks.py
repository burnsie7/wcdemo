import datetime
import decimal
import logging
import random
import string
import time

import requests

from math import sin

from celery.decorators import periodic_task, task
from celery.task.schedules import crontab

from django.conf import settings

from perfdemo.demo.models import Maker, Widget, Order


logger = logging.getLogger(__name__)


rand_str = lambda l: ''.join([random.choice(string.lowercase) for i in xrange(l)])


@task(name="create_maker")
def create_maker():
    name = rand_str(20)
    desc = rand_str(50)
    Maker.objects.create(name=name, description=desc)


@task(name="create_widget")
def create_widget():
    name = 'widget_' + rand_str(12)
    desc = rand_str(50)
    cost = float(decimal.Decimal(random.randrange(100, 999999))/100)
    count = Maker.objects.all().count()
    maker =  Maker.objects.all()[random.randint(0, count-1)]
    Widget.objects.create(name=name, description=desc, cost=cost, maker=maker)


@task(name="create_order")
def create_order():
    name = 'order_' + rand_str(12)
    count = Widget.objects.all().count()
    widget = Widget.objects.all()[random.randint(0, count-1)]
    Order.objects.create(name=name, widget=widget)


@task(name="get_all_orders")
def get_all_orders():
    requests.get('http://127.0.0.1:8000/api/order/')


@task(name="get_order")
def get_order(oid):
    url = 'http://127.0.0.1:8000/api/order/{}'.format(oid)
    requests.get(url)


@task(name="not_found")
def not_found():
    requests.get('http://127.0.0.1:8000/not/found/')


@task(name="throw_error")
def throw_error():
    requests.get('http://127.0.0.1:8000/api/error/')


@task(name="long_query")
def long_query():
    requests.get('http://127.0.0.1:8000/api/long/')


@task(name="traffic_spike")
def traffic_spike():
    oid = Order.object.random_index()
    for i in range(random.randint(1,5) * 1000):
        get_order.delay(oid)


@periodic_task(
    run_every=(crontab(minute='*')),  # crontab(minute=0, hour=5) to run every day midnight EST
    name="request_nonsense",
    ignore_result=True
)
def request_nonsense():
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute

    degrees = ((60 * h + m) // 4) + random.randint(1, 10)
    y = math.sin(math.radians(degrees)) * random.random() * 2

    dow = now.weekday()
    if dow == 0 or dow == 6:
        y = y / (1.5+random.random())
    else:
        y = y * (1.5+random.random())

    if y < 0:
        y = y / 4

    y = (y + 10) * 10

    oid = Order.object.random_index()
    for i in y:
        if i % 35 == 0:
            traffic_spike.delay()
        if i % 21 == 0:
            long_query.delay()
        if i % 11 == 0:
            do_error.delay()
        if i % 7:
            not_found.delay()
        if i % 5:
            get_all_orders.delay()
        get_order.delay(args=[oid])
