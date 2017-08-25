import datetime
import decimal
import logging
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


@task(name="get_makers")
def get_makers():
    requests.get('http://127.0.0.1:8000/api/maker/')


@task(name="get_widgets")
def get_widgets():
    requests.get('http://127.0.0.1:8000/api/widget/')


@task(name="get_orders")
def get_orders():
    requests.get('http://127.0.0.1:8000/api/order/')


@periodic_task(
    run_every=(crontab(minute='*')),  # crontab(minute=0, hour=5) to run every day midnight EST
    name="request_nonsense",
    ignore_result=True
)
def request_nonsense():
    num_requests = random.randint(0, 5)
    hod = datetime.datetime.utcnow().hour
    dow = datetime.datetime.utcnow().weekday()
    multiple = 2
    if dow == 5 or dow == 6:
        multiple = 1
    if hod < 8:
        multiple = hod + 1 * multiple
    elif hod < 14:
        multiple = hod + 2 * multiple
    else:
        hod = (24 - hod) * multiple
    rando = random.randint(0, 4)
    num_requests = num_requests * multiple * rando
    logger.info("num_requests = {}".format(num_requests))
    for x in range(30):  # repeat every second
        time.sleep(2)
        logger.info("x in range = {}".format(x))
        for i in range(num_requests):
            logger.info("i in num_requests = {}".format(i))
            if i % 2 == 0:
                get_orders.delay()
            if i % 3 == 0:
                get_widgets.delay()
            if i % 5 == 0:
                get_makers.delay()
