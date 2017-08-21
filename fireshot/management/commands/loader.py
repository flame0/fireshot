import os
import zipfile
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from travel.models import User, Location, Visit


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default="")

    def handle(self, *args, **options):
        path = options['path']
        data_dir = settings.BASE_DIR
        zip_ref = zipfile.ZipFile(path + 'data.zip', 'r')
        zip_ref.extractall(data_dir)
        zip_ref.close()
        for filename in os.listdir(data_dir +'/data'):
            if filename.endswith(".json"):
                # print(os.path.join(directory, filename))
                with open(filename) as f:
                    print(filename)

            else:
                continue