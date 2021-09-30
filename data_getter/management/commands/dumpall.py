import logging

from django.core.management.base import BaseCommand
from utils import dump, get_models
import datetime
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Dumps all data from the database.'

    def handle(self, *args, **options):
        models = get_models()

        for model in models:
            try:
                earliest_datetime = model.objects.earliest('datetime').datetime
                latest_datetime = model.objects.latest('datetime').datetime
            except model.DoesNotExist:
                print(f'No data found for model {model.__name__}')
                continue

            current_datetime = earliest_datetime

            while current_datetime <= latest_datetime + datetime.timedelta(days=1):
                date = current_datetime.strftime('%Y-%m-%d')
                call_command('dump', date, '--delete')
                current_datetime = current_datetime + datetime.timedelta(days=1)

        print('All data objects dumped to S3 and removed from Django database.')
