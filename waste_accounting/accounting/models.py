from django.db import models
from django.contrib.auth.models import User
import os
import waste_accounting.settings as settings

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    branch = models.ForeignKey('NameOfBranch', on_delete=models.PROTECT, null=True, verbose_name="Филиал")
    department = models.CharField(max_length=150, verbose_name="Подразделение")
    function = models.CharField(max_length=150, verbose_name="Должность")

class NameOfBranch(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование Филиала")
    adress = models.CharField(max_length=300, verbose_name="Адресс Филиала")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'
        ordering = ['pk']

class NameOfObjects(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование объекта")
    branch = models.ForeignKey('NameOfBranch', on_delete=models.PROTECT, null=True, verbose_name="Филиал")
    adress = models.CharField(max_length=300, verbose_name="Адресс Филиала")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['pk']

class Waste (models.Model):
    name = models.CharField(max_length=300, verbose_name="Наименование вида отхода")
    number = models.IntegerField(verbose_name="Номер")
    code_fkko = models.IntegerField(verbose_name="Код по ФККО")
    danger_class = models.IntegerField(verbose_name="Класс опасности вида отхода")
    origin = models.CharField(max_length=300, verbose_name="Происхождение или условия образования вида отхода")
    condition = models.CharField(max_length=300, verbose_name="Агрегатное состояние и физическая форма вида отхода")
    structure = models.CharField(max_length=300, verbose_name="Химический и (или) компонентный состав вида отхода, %")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отход'
        verbose_name_plural = 'Отходы'
        ordering = ['number']

class EducatedWaste (models.Model):
    name = models.ForeignKey('Waste', on_delete=models.PROTECT, null=True, verbose_name="Наименование вида отхода")
    object_name = models.ForeignKey('NameOfObjects', on_delete=models.PROTECT, null=True,
                                    verbose_name="Наименование объекта")
    quantity = models.FloatField(verbose_name="Количество, тонн")
    date_of_educated = models.DateField(verbose_name="Дата образования")
    user_name = models.CharField(max_length=150, verbose_name="Кто внес запись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата внесения записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата внесения записи")
    branch = models.ForeignKey('NameOfBranch', on_delete=models.PROTECT, null=True, verbose_name="Филиал")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'образованные отходы'
        verbose_name_plural = 'образованные отходы'
        ordering = ['name']

class ReclaimedWaste (models.Model):
    name = models.ForeignKey('Waste', on_delete=models.PROTECT, null=True, verbose_name="Наименование вида отхода")
    object_name = models.ForeignKey('NameOfObjects', on_delete=models.PROTECT, null=True, verbose_name="Наименование объекта")
    quantity = models.FloatField(verbose_name="Количество, тонн")
    date_of_reclaimed = models.DateField(verbose_name="Дата образования")
    user_name = models.CharField(max_length=150, verbose_name="Кто внес запись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата внесения записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата внесения записи")
    branch = models.ForeignKey('NameOfBranch', on_delete=models.PROTECT, null=True, verbose_name="Филиал")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'утилизированные отходы'
        verbose_name_plural = 'утилизированные отходы'
        ordering = ['name']


class TransferredWaste(models.Model):
    name = models.ForeignKey('Waste', on_delete=models.PROTECT, null=True, verbose_name="Наименование вида отхода")
    object_name = models.ForeignKey('NameOfObjects', on_delete=models.PROTECT, null=True,
                                    verbose_name="Наименование объекта")
    quantity = models.FloatField(verbose_name="Количество, тонн")
    date_of_transferred = models.DateField(verbose_name="Дата образования")
    user_name = models.CharField(max_length=150, verbose_name="Кто внес запись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата внесения записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата внесения записи")
    type_transferr = models.ForeignKey('TypeTransferr', on_delete=models.PROTECT, null=True, verbose_name="Передача для...")
    branch = models.ForeignKey('NameOfBranch', on_delete=models.PROTECT, null=True, verbose_name="Филиал")
    counterparty = models.ForeignKey('Counterparties', on_delete=models.PROTECT, null=True, verbose_name="Контрагент")


    def __str__(self):

        return self.name

    class Meta:
        verbose_name = 'переданные отходы'
        verbose_name_plural = 'переданные отходы'
        ordering = ['date_of_transferred']

class TypeTransferr(models.Model):
    name = models.CharField(max_length=150, verbose_name="Передача для...")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
        ordering = ['name']

class Counterparties (models.Model):
    name = models.CharField(max_length=300, verbose_name="Наименование контрагента")
    date_of_contract = models.DateField(verbose_name="Дата договора")
    number_of_contract  = models.CharField(max_length=150, verbose_name="Номер договора")
    term_of_contract = models.DateField(verbose_name="Срок договора")
    requisites = models.CharField(max_length=500, verbose_name="Реквизиты")
    intelligence = models.CharField(max_length=500, verbose_name="Сведения")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'
        ordering = ['name']


class Report(models.Model):
    user = models.CharField(max_length=150, verbose_name="Юзер")
    report = models.FileField()
    created_at = models.DateField(auto_now_add=True, verbose_name="Создано")

    def __unicode__(self):

        return '%s' % (self.report.name)


    def delete(self, *args, **kwargs):

        os.remove(os.path.join(settings.BASE_DIR, self.report.name))
        super(Report, self).delete(*args, **kwargs)