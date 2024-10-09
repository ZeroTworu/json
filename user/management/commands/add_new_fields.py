from copy import deepcopy

from django.core.management.base import BaseCommand
from rest_framework import serializers

from user.models import User

import importlib

STEPS_COUNT = 26

serializers_list = []

for i in range(1, 26):
    module_name = f'user.serializers.form.step{i}'
    serializer_name = f'Step{i}Serializer'
    module = importlib.import_module(module_name)
    serializer_class = getattr(module, serializer_name)
    serializers_list.append(serializer_class)


assert len(serializers_list) == 26


class SimpleList(list):
    pass


def get_field_type_and_default_value(field_instance) -> tuple:
    if isinstance(field_instance, (serializers.CharField, serializers.ChoiceField)):
        return str, "-"
    elif isinstance(field_instance, serializers.BooleanField):
        return bool, False
    elif isinstance(field_instance, (serializers.IntegerField, serializers.FloatField, serializers.DecimalField)):
        return int, 0
    elif isinstance(field_instance, serializers.ListSerializer):
        return list, []
    elif isinstance(field_instance, serializers.Serializer):
        return dict, {}
    elif isinstance(field_instance, serializers.ListField):
        return SimpleList, []
    else:
        return None, None


def get_serializer_fields_with_types_and_defaults(serializer):
    field_info = []

    for field_name, field_instance in serializer.fields.items():
        field_type, default_value = get_field_type_and_default_value(field_instance)
        if field_type is None:
            raise ValueError(f"Field is not recognized! - ({field_name},{field_instance})")
        if isinstance(field_instance, serializers.ListSerializer):
            child_fields = get_serializer_fields_with_types_and_defaults(field_instance.child)
            field_info.append((field_name, field_type, child_fields))
        elif isinstance(field_instance, serializers.Serializer):
            child_fields = get_serializer_fields_with_types_and_defaults(field_instance.__class__())
            field_info.append((field_name, field_type, child_fields))
        else:
            field_info.append((field_name, field_type, default_value))
    return field_info


class Command(BaseCommand):
    help = "Migration of json fields to each user"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting to add new fields"))
        steps_with_fields = []
        for serializer in serializers_list:
            steps_with_fields.append(get_serializer_fields_with_types_and_defaults(serializer()))
        for user in User.objects.all():
            for step_index, step_with_fields in enumerate(steps_with_fields):
                step_str = f'step{step_index + 1}'
                user_step = getattr(user, step_str)
                if not user_step:
                    continue
                any_field_updated = False
                for field_data in step_with_fields:
                    field_updated = self.update_field(
                        user_step, field_data
                    )
                    if field_updated:
                        any_field_updated = True
                if any_field_updated:
                    self.stdout.write(self.style.SUCCESS(
                        f"user_id={user.id}, fields updated in {step_str}"))
                setattr(user, step_str, user_step)

            user.save()

    def update_field(self, dict_to_update: dict, field_data: tuple) -> bool:
        field_name, field_type, default_value = field_data
        if field_name in dict_to_update:
            nested_field = deepcopy(dict_to_update[field_name])
            if not nested_field:
                return False
            if field_type == dict:
                for dict_data in default_value:
                    self.update_field(
                        nested_field, dict_data
                    )
                if self.is_same_dicts(dict_to_update[field_name], nested_field):
                    return False
                dict_to_update[field_name] = nested_field
                return True
            elif field_type == list:
                updated_list_data = []
                for existing_list_data in nested_field:
                    for list_data in default_value:
                        self.update_field(existing_list_data, list_data)
                    updated_list_data.append(existing_list_data)
                if self.is_same_dicts(dict_to_update[field_name], updated_list_data):
                    return False
                dict_to_update[field_name] = updated_list_data
                return True
        elif field_type == list:
            dict_to_update[field_name] = []
            return True
        elif field_type == dict:
            dict_to_update[field_name] = {}
            return True
        else:
            dict_to_update[field_name] = default_value
            return True

    def is_same_dicts(self, dict1, dict2) -> bool:
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            if dict1.keys() != dict2.keys():
                return False
            return all(self.is_same_dicts(dict1[key], dict2[key]) for key in dict1)
        elif isinstance(dict1, list) and isinstance(dict2, list):
            if len(dict1) != len(dict2):
                return False
            return all(self.is_same_dicts(item1, item2) for item1, item2 in zip(dict1, dict2))
        return True
