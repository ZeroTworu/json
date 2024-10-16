
# Дефолтные значения для полей из сериалайзера
# CharField = "-"
# BooleanField = False
# IntegerField (or any number field) = 0
# ListSerializer = []
# Serializer = {...} - Все поля из сериалайзера
# ListField = []

# Чтобы достать поля из сериалайзера
# SerializerClass().fields.items():


from user.json_service import JsonService
from user.models import BasicUser


class JsonMigrator:
    @classmethod
    def migrate(cls):
        users = BasicUser.objects.all()
        for user in users:
            service = JsonService(user)
            service.update()


