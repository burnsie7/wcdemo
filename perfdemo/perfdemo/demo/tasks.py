import datetime
import decimal
import logging
import math
import random
import string
import time

import requests

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
    url = 'http://127.0.0.1:8000/api/order/?id={}'.format(oid)
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
def traffic_spike(num):
    oid = get_random_order_id()
    for i in range(random.randint(1,5) * num):
        get_order.delay(oid)

@periodic_task(
    run_every=(crontab(minute='*')),  # crontab(minute=0, hour=5) to run every day midnight EST
    name="request_nonsense",
    ignore_result=True

def request_nonsense():
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    mag = 20
    degrees = ((60 * h + m) // 4) + random.randint(1, 10)
    y = math.sin(math.radians(degrees)) * random.random() * 2

    dow = now.weekday()
    if dow == 0 or dow == 6:
        y = y / (1.5+random.random())
    else:
        y = y * (1.5+random.random())

    if y < 0:
        y = y / 4

    y = int(math.floor((y + 10) * mag))

    trick = random.randint(1, 100)
    if trick == 33:
        traffic_spike.delay(mag*2)
    if trick == 21:
        for i in range(mag):
            long_query.delay()
    if trick == 55:
        for i in range(mag):
            throw_error.delay()

    oid = get_random_order_id()
    sleep_time = 60.0 / y
    for i in range(1, y):
        if i % 11 == 0:
            throw_error.delay()
        if i % 7 == 0:
            not_found.delay()
        if i % 5 == 0:
            get_all_orders.delay()
        get_order.delay(oid)
        time.sleep(sleep_time))
