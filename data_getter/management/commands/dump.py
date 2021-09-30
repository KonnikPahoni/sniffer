from django.core.management.base import BaseCommand
from utils import dump


class Command(BaseCommand):
    help = 'Dumps the database for the specified date.'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+', type=str)

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete objects after successful backup.',
        )

    def handle(self, *args, **options):
        dump(options['date'][0], options['delete'])
