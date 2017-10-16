import datetime
import decimal
import logging
import math
import random
import string
import time

import requests
import grequests

from celery.decorators import periodic_task, task
from celery.task.schedules import crontab

from django.conf import settings

from perfdemo.demo.models import Maker, Widget, Order

from ddtrace import tracer

logger = logging.getLogger(__name__)


rand_str = lambda l: ''.join([random.choice(string.lowercase) for i in xrange(l)])
BASE_URL = 'http://' + settings.MY_SVC_NAMESPACE + ':' + settings.MY_SVC_PORT


def get_random_order_id():
    return random.choice(Order.objects.all()).id


@task(name="create_maker_task")
@tracer.wrap(service='create-maker')
def create_maker():
    name = rand_str(20)
    desc = rand_str(50)
    Maker.objects.create(name=name, description=desc)


@task(name="create_widget_task")
@tracer.wrap(service='create-widget')
def create_widget():
    name = 'widget_' + rand_str(12)
    desc = rand_str(50)
    cost = float(decimal.Decimal(random.randrange(100, 999999))/100)
    count = Maker.objects.all().count()
    maker =  Maker.objects.all()[random.randint(0, count-1)]
    Widget.objects.create(name=name, description=desc, cost=cost, maker=maker)


@task(name="create_order_task")
@tracer.wrap(service='create-order')
def create_order():
    name = 'order_' + rand_str(12)
    count = Widget.objects.all().count()
    widget = Widget.objects.all()[random.randint(0, count-1)]
    Order.objects.create(name=name, widget=widget)

def get_url(n, ustr):
    urls = []
    for i in range(n):
        urls.append(BASE_URL + ustr)
    rs = (grequests.get(u) for u in urls)
    grequests.map(rs)

def get_formatted_url(oid, n, ustr):
    urls = []
    for i in range(n):
        urls.append(BASE_URL + ustr + '{}/'.format(oid))
    rs = (grequests.get(u) for u in urls)
    grequests.map(rs)

@periodic_task(
    run_every=(crontab(minute='*')),  # crontab(minute=0, hour=5) to run every day midnight EST
    name="request_nonsense_task",
    ignore_result=True
)
@tracer.wrap(service='request-generator')
def request_nonsense():
    now = datetime.datetime.now() - datetime.timedelta(hours=6)  # Offset for UTC
    h = now.hour
    m = now.minute
    mag = settings.REQ_MULTIPLE
    degrees = ((60 * h + m) // 4) + random.randint(1, 10)
    y = math.sin(math.radians(degrees)) * random.random() * 2

    dow = now.weekday()
    if dow == 5 or dow == 6:  # Looks like AWS uses 0 for monday
        y = y / (1.5+random.random())
    else:
        y = y * (1.5+random.random())

    if y < 0:
        y = y / 4

    y = int(math.floor((y + 10) * mag))

    trick = random.randint(1, 100)
    if trick == 33:
        traffic_spike(mag*2)
    if trick == 21:
        get_url(mag, '/api/long/')
    if trick == 55:
        get_url(mag, '/api/error/')

    oid = get_random_order_id()
    sleep_time = 60.0 / y

    for i in range(1, y):
        get_formatted_url(oid, 1, '/api/order/')
        if i % 11 == 0:
            get_url(1, '/api/error/')
        if i % 7 == 0:
            get_url(1, '/not/found/')
        if i % 5 == 0:
            get_url(1, '/api/order/')
        time.sleep(sleep_time)
