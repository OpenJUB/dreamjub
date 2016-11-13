from django.core.management import base
from dreamjub import models


class Command(base.BaseCommand):
    help = 'Loads all pictures from IRC-IT servers. '

    def handle(self, *args, **options):
        models.Student.refresh_images()
