from rest_framework import serializers


class Step1Serializer(serializers.Serializer):
    lastname = serializers.CharField(max_length=255, help_text='Фамилия')
    name = serializers.CharField(max_length=255, help_text='Имя')
    is_fio_changed = serializers.BooleanField(help_text='Вы меняли свои ФИО?')
    prev_name = serializers.ListField(child=serializers.CharField(), help_text='Укажите предыдущее имя')
    prev_lastname = serializers.ListField(child=serializers.CharField(), help_text='Укажите предыдущую фамилию')
    prev_surname = serializers.ListField(child=serializers.CharField(), help_text='Укажите предыдущее отчество')
    is_rf_citizenship = serializers.BooleanField(help_text='Гражданство')
    in_rf_justification = serializers.ChoiceField(choices=['РВП', 'ВНЖ', 'Виза', 'Миграционная карта', '-'],
                                                  help_text='Укажите основание нахождения в Российской Федерации')
    gender = serializers.ChoiceField(choices=['Мужчина', 'Женщина'], help_text='Ваш пол')
    house = serializers.CharField(max_length=255, allow_blank=True, help_text='Дом')
    block = serializers.CharField(max_length=255, allow_blank=True, help_text='Корпус')
    apartment = serializers.CharField(max_length=255, allow_blank=True, help_text='Квартира')
    is_temp_address_factual = serializers.BooleanField(
        help_text='Адрес временной регистрации совпадает адресом фактического проживания')

    class JobSerializer(serializers.Serializer):
        class JobSerializer2(serializers.Serializer):
            name = serializers.CharField(max_length=255, help_text='Укажите наименование работадателя')
            position = serializers.CharField(max_length=255, help_text='Укажите вашу должность')
            avg_salary = serializers.FloatField(help_text='Укажите ваш среднемесячный доход по 2-Ндфл')
        name = serializers.CharField(max_length=255, help_text='Укажите наименование работадателя')
        position = serializers.CharField(max_length=255, help_text='Укажите вашу должность')
        nested = JobSerializer2()

    new_jobs_list_field = serializers.ListSerializer(
        child=JobSerializer(),
        help_text='Работы'
    )
    new_jobs_dict_field = JobSerializer()


class Step2Serializer(serializers.Serializer):
    class JobSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, help_text='Укажите наименование работадателя')
        position = serializers.CharField(max_length=255, help_text='Укажите вашу должность')
        avg_salary = serializers.FloatField(help_text='Укажите ваш среднемесячный доход по 2-Ндфл')

    work_status = serializers.ChoiceField(
        choices=['Трудоустроен', 'Безработный'],
        help_text='Укажите ваш трудовой статус'
    )
    is_in_czn = serializers.BooleanField(help_text='Стоите ли вы на учете в Центре Занятости Населения?')
    jobs = serializers.ListSerializer(
        child=JobSerializer(),
        help_text='Работы'
    )
    individual_worker_status = serializers.ChoiceField(
        choices=['Открыто сейчас', 'Закрыто в течение последних 3 лет', 'Закрыто более 3 лет назад', 'Никогда не было',
                 '-'],
        help_text='Укажите ваш статус Индивидуального предпринимателя'
    )
    is_self_employed = serializers.BooleanField(help_text='Наличие статуса самозанятого')
    self_employed_income_way = serializers.ChoiceField(
        choices=['Наличные', 'На свою банковскую карту', 'На чужую банковскую карту', '-'],
        help_text='Как получаете доход по самозанятости?'
    )
    avg_monthly_salary = serializers.FloatField(help_text='Укажите среднемесячную сумму дохода в рублях')


class Step3Serializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
