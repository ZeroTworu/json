from importlib import import_module
from typing import TYPE_CHECKING

from rest_framework.fields import empty

from user.models import BasicUser

if TYPE_CHECKING:
    from typing import Any

    from rest_framework.serializers import Serializer


class JsonService:

    def __init__(self, user: 'BasicUser'):
        self._user: 'BasicUser' = user
        self._model_field: 'dict' = {}
        self._field: 'dict|list' = {}
        self._serializer: 'Serializer|None' = None  # Сериалайзер с которым работаем прямо сейчас
        self._base_serializer: 'Serializer|None' = None  # Сериалайзер который мы импортнули динамически
        self._keys: 'list' = []

    def update(self):
        for field in self._user._meta.fields:

            if field.__class__.__name__ != 'JSONField':
                continue

            serializers = import_module('user.serializers')
            try:
                serializer_class = getattr(serializers, f'{field.name.capitalize()}Serializer')
            except AttributeError as exc:
                continue
            self.update_model_field(field.name, serializer_class)

    def update_model_field(self, field_name: 'str', serializer_class):
        self._model_field: 'dict' = getattr(self._user, field_name)

        if not self._model_field:
            return

        self._serializer = serializer_class()
        self._base_serializer = serializer_class()
        self._field = self._model_field.copy()
        self._update_dict()
        setattr(self._user, field_name, self._field)
        self._user.save()

    def _update_dict(self):
        for name, _type in self._serializer.get_fields().items():
            self._keys.append(name)
            match _type.__class__.__name__:
                case 'CharField' | 'BooleanField' | 'IntegerField' | 'ChoiceField' | 'ListField':
                    self._update_simple(name)
                case 'DictSerializer' | 'DictNestedSerializer':
                    self._update_dict_field(name)
                case 'ListSerializer':
                    self._update_list_field(name)
        self._serializer = self._base_serializer

    def _get_default(self, name: 'str', value_name: 'str'):
        match name:
            case 'CharField':
                return '-'
            case 'BooleanField':
                return False
            case 'IntegerField':
                return 0
            case 'ChoiceField':
                value = self._serializer.get_fields().get(value_name).default
                if value is empty:
                    return '-'
                return value
            case 'ListField':
                return []
            case _:
                return None

    def _update_simple(self, value_name: 'str'):
        if self._has_value():
            self._keys.pop()
            return
        filed = self._serializer.get_fields().get(value_name)
        value = self._get_default(filed.__class__.__name__, value_name)
        self._set_value(value)
        print(f'User {self._user.pk}', '.'.join(self._keys), f'set value {value}')
        self._keys.pop()

    def _update_list_field(self, value_name: 'str'):
        if not self._has_value():
            self._set_value([{}])
        field = self._base_serializer.get_fields().get(value_name)
        self._serializer = field.child
        self._update_dict()
        self._keys.pop()

    def _update_dict_field(self, value_name: 'str'):
        if not self._has_value():
            self._set_value({})
        self._serializer = self._serializer.get_fields().get(value_name)
        self._update_dict()
        self._keys.pop()

    def _has_value(self, _dict: 'dict' = None, index: 'int' = 0) -> 'bool':
        if _dict is None:
            _dict = self._field
        keys = self._keys[index:]
        for index, key in enumerate(keys):
            value = _dict.get(key)
            if value is None:
                return False
            if isinstance(value, list) and index < len(keys):
                for item in value:
                    if isinstance(item, dict):
                        return self._has_value(item, index)
                return True
            if isinstance(value, dict) and index < len(keys):
                return self._has_value(value, index)

    def _set_value(self, value: 'Any', _dict: 'dict' = None, index: 'int' = 0):
        if _dict is None:
            _dict = self._field
        keys = self._keys[index:]
        for index, key in enumerate(keys):
            current_value = _dict.get(key)
            if current_value is None:
                _dict[key] = value
            if isinstance(current_value, list) and index < len(keys):
                for item in current_value:
                    if isinstance(item, dict):
                        self._set_value(value, item, index)
            if isinstance(current_value, dict) and index < len(keys):
                self._set_value(value, current_value, index)

