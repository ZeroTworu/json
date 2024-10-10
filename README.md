## Тестовое задание для миграции полей из сериалайзера в JSON поля пользователей.

# Инструкция к коду:
    1. Откройте файл user.models, здесь находится модель BasicUser, у которой есть 2 JSON поля.
    2. Откройте файл user.serializers, здесь находятся два сериалайзера,
        которые относяткся к первому и второму шагам (BasicUser.step1, BasicUser.step2).
        Схема этих полей всегда будет совпадать с полями внутри сериалайзеров.
    3. Откройте файл user.migrator. Здесь находится класс JsonMigrator.
        Весь ваш код должен быть написан в этом файле.

# Первые шаги

## 1. Запустите миграцию
    python manage.py migrate

## 2. Запустите команду
    python manage.py migrate_json

#### Данная команда очистит базу и создаст 10 объектов BasicUser в базе и выведет print. 
#### У каждого юзера поле step1 будет заполнено на 1 значение, но поле step2 будет пустым.


# Задача

    Каждый шаг внутри BasicUser создается через сериалайзеры. 
    Это значит, что эти JSON поля всегда должны иметь каждое поле из соответствующего сериалайзера.
    Представьте сценарий, что у вас внутри сериалайзера Step1Serializer было 5 полей и вы создали 100 пользователей,
    у которых step1 имеет 5 ключей внутри (все из Step1Serializer). Далее, вам нужно добавить новое поле в сериалайзер
    Step1Serializer. В этом случае, все ваши старые пользователи не будут иметь новое поле внутри step1.
    Суть задачи - напишите код, который мигрирует все новые поля из
    всех сериалайзеров в нужные шаги для пользователей c дефолтным значением.
    
# Пример
    У вас есть сериалайзеры:
    
``` python
class Step1Serializer(serializers.Serializer):
    class DictSerializer(serializers.Serializer):
        class DictNestedSerializer(serializers.Serializer):
            string_field = serializers.CharField(max_length=255)
            boolean_field = serializers.BooleanField()
            list_field = serializers.ListField(child=serializers.CharField())
            choice_field = serializers.ChoiceField(choices=['1', '2', '3', '-'])

        string_field = serializers.CharField(max_length=255)
        boolean_field = serializers.BooleanField()
        list_field = serializers.ListField(child=serializers.CharField())
        choice_field = serializers.ChoiceField(choices=['1', '2', '3', '-'])
        dict_field = DictNestedSerializer()

    string_field = serializers.CharField(max_length=255)
    boolean_field = serializers.BooleanField()
    list_field = serializers.ListField(child=serializers.CharField())
    choice_field = serializers.ChoiceField(choices=['1', '2', '3', '-'], default="2")
    dict_field = DictSerializer()
    list_dict_field = serializers.ListSerializer(
        child=DictSerializer()
    )
    empty_list_dict_field = serializers.ListSerializer(
        child=DictSerializer()
    )
  
class Step2Serializer(serializers.Serializer):
    ...
```

#### У вас есть пользователь с шагами:

``` python
step1 = {
    "string_field": "Британская кошка",
    "boolean_field": False,
    "list_dict_field": [
        {
            "string_field": "test"
        }
    ]
}

step2 = {}
```

    Как вы уже могли заметить, в step1 не хватает многих полей из Step1Serializer. 
    После миграции - все новые поля должны появиться внутри step1.
    ВАЖНО - новые поля должны быть мигрированы на всех уровнях вложенности. Будь это dict, ListSerializer.
    Но, step2 у пользователя пустой - а значит,
    он никогда не был заполнен и его при миграции оставляем пустым.


#### Результаты после миграции:

``` python
step1 = {
    "string_field": "Британская кошка",
    "boolean_field": False,
    "list_field" : [],
    "choice_field": "2",
    "dict_field": {
        "string_field": "1",
        "boolean_field": False,
        "list_field" : [],
        "choice_field": "-",
        "dict_field": {
            "string_field": "-",
            "boolean_field": False,
            "list_field" : [],
            "choice_field": "-",
        }
    },
    "list_dict_field": [
        {
            "string_field": "test",
            "string_field": "-",
            "boolean_field": False,
            "list_field" : [],
            "choice_field": "-",
            "dict_field": {
                "string_field": "-",
                "boolean_field": False,
                "list_field" : [],
                "choice_field": "-",
            }
        }
    ],
    "empty_list_dict_field": []
}

step2 = {}
```

#### Обратите внимание - поле `dict_field` внутри `step1` полностью появилось со всеми ключами. А также все вложенные структуры тоже появились/обновились.  Поле `list_dict_field` также полностью добавило все новые поля в свой элемент, но `empty_list_dict_field`  остался пустым. А также, поле `step1.choice_field` имеет значение '2', потому что внутри сериалайзера в этом поле есть параметр `default`. Если мы имеем этот параметр внутри поля, мы используем его, как дефолтное значение. Если его нет - берем из статичных значений.

# Правила для полей
    1. Дефолтные значения для полей будут прописаны в файле `user.migrator`
    2. Если тип поля dict (на подобии DictSerializer()) - мы всегда его добавляем в шаг, независимо от того, есть это поле частично/ или его вообще нет.
    3. Если тип поле list (на подобии ListSerializer()) - мы обновляем все его существующие элементы. Если этого поля нет, или же оно пустое, то мы оставляем его пустым, то есть просто [].


# Бонусные задания (Не обязательное)

### 1. При миграции, нужно выводить, какое именно поле и в каком шаге, для какого юзера было добавлено.
    Пример: 
    User with id 1, step1.list_field added
    User with id 1, step1.dict_field.dict_field.choice_field added 
    ...
### 2. Если нам придется добавить новое поле в модель пользователя, step3, step4, ..., а также сериалайзеры к ним - мы не должны лезть в файл user.migrator, чтобы указать эти шаги и сериалайзеры. Мигратор сам должен их увидеть.
