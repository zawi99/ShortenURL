from django.core.management.base import BaseCommand
from shortener.models import ShrtnURL


class Command(BaseCommand):
    help = 'Refreshes all ShrtnURL shortcodes'

    def add_arguments(self, parser):  # add argument 'items'
        parser.add_argument('items', type=int)

    def handle(self, *args, **options):  # change shortcodes, items == how many to change
        return ShrtnURL.objects.refresh_shortcodes(items=options['items'])
