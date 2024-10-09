from django.core.management.base import BaseCommand
from user.models import BasicUser

# CharField = "-"
# BooleanField = False
# IntegerField (or any number field) = 0
# ListSerializer = []
# Serializer = {}
# ListField = []

# Чтобы достать поля из сериалайзера
# SerializerClass().fields.items():


class Command(BaseCommand):
    help = "Migration of json fields to each user"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting to add new fields"))
        users = BasicUser.objects.all()
        for user in users:
            print(f'STEP1 - {user.step1}')
            print(f'STEP2 - {user.step2}')
            print(f'STEP3 - {user.step3}')