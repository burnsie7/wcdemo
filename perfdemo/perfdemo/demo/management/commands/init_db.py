from django.core.management.base import BaseCommand, CommandError

from perfdemo.demo.tasks import create_order, create_widget, create_maker

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for i in range(50):
            create_maker()

        for i in range(100):
            create_widget()

        for i in range(200):
            create_order()
