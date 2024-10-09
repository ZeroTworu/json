from rest_framework import serializers


class Step1Serializer(serializers.Serializer):
    lastname = serializers.CharField(max_length=255, help_text='Фамилия')
    name = serializers.CharField(max_length=255, help_text='Имя')
    surname = serializers.CharField(max_length=255, help_text='Отчество')
    is_fio_changed = serializers.BooleanField(help_text='Вы меняли свои ФИО?')
    is_name_changed = serializers.BooleanField(help_text='Что вы изменяли? Имя')
    is_lastname_changed = serializers.BooleanField(help_text='Что вы изменяли? Фамилия')
    is_surname_changed = serializers.BooleanField(help_text='Что вы изменяли? Отчество')
    prev_name = serializers.ListField(child=serializers.CharField(), help_text='Укажите предыдущее имя')
    prev_lastname = serializers.ListField(child=serializers.CharField(), help_text='Укажите предыдущую фамилию')
    prev_surname = serializers.ListField(child=serializers.CharField(), help_text='Укажите предыдущее отчество')
    is_rf_citizenship = serializers.BooleanField(help_text='Гражданство')
    in_rf_justification = serializers.ChoiceField(choices=['РВП', 'ВНЖ', 'Виза', 'Миграционная карта', '-'],
                                                  help_text='Укажите основание нахождения в Российской Федерации')
    gender = serializers.ChoiceField(choices=['Мужчина', 'Женщина'], help_text='Ваш пол')
    dob = serializers.CharField(max_length=255, allow_blank=True, help_text='Дата рождения')
    birth_place = serializers.CharField(max_length=255, allow_blank=True, help_text='Место рождения')
    document_series = serializers.CharField(max_length=255, allow_blank=True, help_text='Серия и номер паспорта')
    document_date = serializers.CharField(max_length=255, allow_blank=True, help_text='Дата выдачи')
    document_given_by = serializers.CharField(max_length=255, allow_blank=True, help_text='Кем выдан')
    code = serializers.CharField(max_length=255, allow_blank=True, help_text='Код подразделения')
    region = serializers.CharField(max_length=255, allow_blank=True, help_text='Регион')
    address = serializers.CharField(max_length=255, allow_blank=True, help_text='Аддресс')
    city = serializers.CharField(max_length=255, allow_blank=True, help_text='Город')
    settlement = serializers.CharField(max_length=255, allow_blank=True, help_text='Населенный пункт')
    street = serializers.CharField(max_length=255, allow_blank=True, help_text='Улица')
    house = serializers.CharField(max_length=255, allow_blank=True, help_text='Дом')
    block = serializers.CharField(max_length=255, allow_blank=True, help_text='Корпус')
    apartment = serializers.CharField(max_length=255, allow_blank=True, help_text='Квартира')
    is_temp_address_factual = serializers.BooleanField(
        help_text='Адрес временной регистрации совпадает адресом фактического проживания')
    factual_region = serializers.CharField(max_length=255, allow_blank=True, help_text='Фактический регион')
    factual_address = serializers.CharField(max_length=255, allow_blank=True, help_text='Фактический аддресс')
    factual_city = serializers.CharField(max_length=255, allow_blank=True, help_text='Фактический город')
    factual_settlement = serializers.CharField(max_length=255, allow_blank=True, help_text='Населенный пункт')
    factual_street = serializers.CharField(max_length=255, allow_blank=True, help_text='Фактический улица')
    factual_house = serializers.CharField(max_length=255, allow_blank=True, help_text='Фактический дом')
    factual_block = serializers.CharField(max_length=255, allow_blank=True, help_text='Фактический корпус')
    factual_apartment = serializers.CharField(max_length=255, allow_blank=True, help_text='Фактический квартира')
    is_inn = serializers.BooleanField(help_text='Есть ли у вас ИНН')
    inn = serializers.CharField(max_length=255, allow_blank=True, help_text='ИНН')
    is_snils = serializers.BooleanField(help_text='Есть ли у вас СНИЛС')
    snils = serializers.CharField(max_length=255, allow_blank=True, help_text='СНИЛС')
    is_ilc = serializers.BooleanField(help_text='Имеете ли вы индивидуальный лицевой счет (ИЛС) в пенсионном фонде РФ?')

    # class JobSerializer(serializers.Serializer):
    #     class JobSerializer2(serializers.Serializer):
    #         name = serializers.CharField(max_length=255, help_text='Укажите наименование работадателя')
    #         position = serializers.CharField(max_length=255, help_text='Укажите вашу должность')
    #         avg_salary = serializers.FloatField(help_text='Укажите ваш среднемесячный доход по 2-Ндфл')
    #     name = serializers.CharField(max_length=255, help_text='Укажите наименование работадателя')
    #     position = serializers.CharField(max_length=255, help_text='Укажите вашу должность')
    #
    # new_jobs_list_field = serializers.ListSerializer(
    #     child=JobSerializer(),
    #     help_text='Работы'
    # )
    # new_jobs_dict_field = JobSerializer()


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
    is_bills_for_fns = serializers.BooleanField(
        help_text='Вносите ли вы чеки по доходу самозанятого в личный кабинет ФНС?')

    # class JobSerializer(serializers.Serializer):
    #     class JobSerializer2(serializers.Serializer):
    #         name = serializers.CharField(max_length=255, help_text='Укажите наименование работадателя')
    #         position = serializers.CharField(max_length=255, help_text='Укажите вашу должность')
    #         avg_salary = serializers.FloatField(help_text='Укажите ваш среднемесячный доход по 2-Ндфл')
    #     name = serializers.CharField(max_length=255, help_text='Укажите наименование работадателя')
    #     position = serializers.CharField(max_length=255, help_text='Укажите вашу должность')
    #
    # new_jobs_list_field = serializers.ListSerializer(
    #     child=JobSerializer(),
    #     help_text='Работы'
    # )
    # new_jobs_dict_field = JobSerializer()
