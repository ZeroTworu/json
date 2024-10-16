from rest_framework import serializers


class DictNestedSerializer(serializers.Serializer):
    string_field = serializers.CharField(max_length=255)
    boolean_field = serializers.BooleanField()
    list_field = serializers.ListField(child=serializers.CharField())
    choice_field = serializers.ChoiceField(choices=['1', '2', '3', '-'])


class DictSerializer(serializers.Serializer):
    string_field = serializers.CharField(max_length=255)
    boolean_field = serializers.BooleanField()
    list_field = serializers.ListField(child=serializers.CharField())
    choice_field = serializers.ChoiceField(choices=['1', '2', '3', '-'])
    dict_field = DictNestedSerializer()


class Step1Serializer(serializers.Serializer):
    string_field = serializers.CharField(max_length=255)
    boolean_field = serializers.BooleanField()
    list_field = serializers.ListField(child=serializers.CharField())
    choice_field = serializers.ChoiceField(choices=['1', '2', '3', '-'], default='2')
    dict_field = DictSerializer()
    list_dict_field = serializers.ListSerializer(
        child=DictSerializer()
    )
    empty_list_dict_field = serializers.ListSerializer(
        child=DictSerializer()
    )


class Step2Serializer(Step1Serializer):
    pass

