"""
Database models for cnot profiles.
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.data import COUNTRIES
from model_utils import Choices
from model_utils.fields import StatusField, UUIDField
from model_utils.models import TimeStampedModel

from cnot.utils import generate_new_filename


class Profile(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    uuid = UUIDField(version=4, editable=False, unique=True)

    SEX = (('m', 'мужской'), ('f', 'женский'))
    DOCUMENT_TYPES = (('u', 'Удостоверение'), ('s', 'Сертификат'), ('n', 'Неуспеваемость'))
    EDUCATION_LEVEL = (('M', 'Среднее профессиональное'), ('H', 'Высшее'))

    last_name = models.CharField("Фамилия", max_length=255, null=False, blank=False)
    first_name = models.CharField("Имя", max_length=255, null=False, blank=False)
    second_name = models.CharField("Отчество", max_length=255, null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=SEX, null=False, blank=False)
    birth_date = models.CharField("Дата рождения", max_length=16, null=False, blank=False)
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)

    city = models.CharField("Город", max_length=256, null=True, blank=False)
    job = models.CharField("Место работы", max_length=2048, null=True, blank=False)
    position = models.CharField("Должность", max_length=2048, null=True, blank=False)

    address_register = models.TextField("Адрес регистрации", blank=True, null=True)

    claim_scan = models.FileField("Скан заявления на зачисление в программу ", upload_to=generate_new_filename,
                                  null=True, blank=True)

    series = models.CharField("Серия", max_length=8, null=True, blank=False)
    number = models.CharField("Номер", max_length=8, null=True, blank=False)
    issued_by = models.TextField("Кем выдан", null=True, blank=False)
    unit_code = models.CharField("Код подразделения", max_length=16, null=True, blank=False)
    issue_date = models.CharField("Дата выдачи", max_length=16, null=True, blank=False)

    education_level = models.CharField("Уровень базового образования", max_length=1, choices=EDUCATION_LEVEL,
                                       null=False, blank=False)

    series_diploma = models.CharField("Серия документа об образовании", max_length=255, null=True, blank=False)
    number_diploma = models.CharField("Номер документа об образовании", max_length=255, null=True, blank=False)
    edu_organization = models.CharField("Образовательное учреждение", max_length=355, null=True, blank=True)
    specialty = models.CharField("Специальность (направление подготовки)", max_length=355, null=True, blank=True)
    year_of_ending = models.CharField("Год окончания", max_length=16, null=True, blank=True)

    all_valid = models.BooleanField("Данные в доках слушателя совпадают и корректны", default=False)

    doc_forwarding = models.FileField("Скан заявление о пересылке удостоверения слушателя почтой России",
                                      upload_to=generate_new_filename, null=True, blank=True)

    leader_id = models.CharField("Leader ID", max_length=355, null=True, blank=True)
    SNILS = models.CharField("Номер СНИЛС", max_length=355, null=True, blank=True)
    add_email = models.EmailField("Почта для связи", max_length=254, null=True, blank=True)

    birth_place = models.CharField("Место рождения", max_length=355, null=True, blank=True)
    job_address = models.CharField("Адрес работы", max_length=355, null=True, blank=True)

    manager = models.CharField("Ответственный", max_length=355, null=True, blank=True)

    mail_index = models.CharField("Почтовый индекс", max_length=255, null=True, blank=True)
    country = models.CharField("Страна", default='Россия', max_length=255, null=True, blank=True)
    address_living = models.TextField("Адрес проживания", max_length=255, blank=True, null=True)

    terms = models.BooleanField("Я принимаю условия использования и соглашаюсь с политикой конфиденциальности",
                                null=False, blank=False)

    user = models.OneToOneField(get_user_model(), unique=True, db_index=True, related_name='verified_profile1',
                                verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    prefered_org = models.CharField("Организация", max_length=255, blank=True, null=True)

    admin_number = models.CharField("Номер согласия", max_length=355, null=True, blank=True)
    admin_diagnostics = models.BooleanField("Диагностики пройдены", default=False)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @classmethod
    def get_profile(cls, user):
        if cls.objects.select_related().filter(user=user).exists():
            return cls.objects.select_related().filter(user=user)
        else:
            return None

    class Meta:
        verbose_name = 'анкета для зачисления'
        verbose_name_plural = 'анкеты для зачисления'

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return f'<Profile, ID: {self.uuid}>'


class Role(models.Model):
    title = models.CharField(_('Title'), max_length=32, unique=True)

    def __str__(self):
        return f'<Role, title: {self.title}>'


class UrFUProfile(TimeStampedModel):
    """
    Main UrFU profile
    """

    COUNTRIES_LIST = tuple((x, COUNTRIES[x]) for x in COUNTRIES.keys())

    EDUCATION_LEVEL = (('M', 'Среднее профессиональное'), ('H', 'Высшее'))
    # USER_TYPES = (('u', 'user or not available'), ('s', 'student'), ('h', 'HR'), ('a', 'admin'))

    user = models.OneToOneField(get_user_model(), unique=True, db_index=True, related_name='verified_profile',
                                verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    roles = models.ManyToManyField(Role)
    # type = models.CharField('User type', max_length=1, choices=USER_TYPES, default='u')
    last_name = models.CharField("Фамилия", max_length=255, null=False, blank=False)
    first_name = models.CharField("Имя", max_length=255, null=False, blank=False)
    second_name = models.CharField("Отчество", max_length=255, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=255, null=False, blank=False)

    SNILS = models.CharField("Номер СНИЛС", max_length=355, null=True, blank=True)
    specialty = models.CharField("Специальность (направление подготовки)", max_length=355)
    country = models.CharField("Гражданство", max_length=2, choices=COUNTRIES_LIST)
    education_level = models.CharField("Уровень базового образования", max_length=1, choices=EDUCATION_LEVEL)
    job = models.CharField("Место работы", max_length=2048)
    position = models.CharField("Должность", max_length=2048)
    birth_date = models.CharField("Дата рождения", max_length=16)

    @property
    def list_roles(self):
        return [role.title for role in self.roles.all()]

    @classmethod
    def get_profile(cls, user):
        if cls.objects.select_related().filter(user=user).exists():
            return cls.objects.select_related().filter(user=user)
        else:
            return None

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f'<UrFUProfile, ID: {self.pk}, Person: {self.last_name} {self.first_name}>'


class LeadRequest(TimeStampedModel):
    """
    Model for store CRM requests
    """
    STATUSES = (
        ('created', 'created'),
        ('sent', 'sent'),
        ('error', 'error')
    )
    method = models.CharField(max_length=32, null=False, blank=False)
    title = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=32, blank=True)
    second_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    status_id = models.CharField(max_length=32, blank=True)
    email = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default=STATUSES[0][0])

    def set_status(self, status):
        self.status = status
        self.save()

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f'<LeadRequest, ID: {self.pk}, Lead: {self.last_name} {self.name}, Status: {self.status}>'

    class Meta:
        verbose_name = 'запрос в Битрикс'
        verbose_name_plural = 'запросы в Битрикс'


class Reflection(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    STATUS = Choices('draft', 'published')
    status = StatusField()

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<Reflection, ID: {}>'.format(self.id)


class Question(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<Question, ID: {}>'.format(self.id)


class Answer(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        # TODO: return a string appropriate for the data fields
        return '<Answer, ID: {}>'.format(self.id)
