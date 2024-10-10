from django.core.management.base import BaseCommand

from user.migrator import JsonMigrator
from user.models import BasicUser


class Command(BaseCommand):
    help = "Migration of json fields to each user"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting of migration"))
        BasicUser.objects.all().delete()
        for i in range(10):
            BasicUser.objects.create(
                step1={"string_field": "test string field"},
                step2={}
            )
        print(
            f'Создано 10 пользователей!\n'
        )
        JsonMigrator.migrate()