from django.db import models
from django.urls import reverse

from authors.models import Author
from colections.models import Collection


class Condition(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True, verbose_name="Код")
    label = models.CharField(max_length=100, verbose_name="Название")
    needs_restoration = models.BooleanField(default=False, verbose_name="Требуется реставрация")
    needs_check = models.BooleanField(default=False, verbose_name="Требуется проверка")

    class Meta:
        db_table = "conditions"
        verbose_name = "Состояние"
        verbose_name_plural = "Состояния"
        ordering = ("id",)

    def __str__(self):
        return self.label

    def get_status(self, is_available=True):
        if self.needs_restoration:
            return "Требуется реставрация"
        if self.needs_check:
            return "Требуется проверка"
        if not is_available:
            return "Недоступен"
        return self.label


class ExhibitQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True)

    def unavailable(self):
        return self.filter(is_available=False)

    def by_condition(self, condition_code):
        return self.filter(condition__code=condition_code)


class Exhibit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Название")

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="exhibits",
        verbose_name="Автор"
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="exhibits",
        verbose_name="Коллекция"
    )

    condition = models.ForeignKey(
        Condition,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Состояние"
    )

    year = models.IntegerField(verbose_name="Год создания")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Стоимость")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")

    objects = ExhibitQuerySet.as_manager()

    class Meta:
        db_table = "exhibits"
        verbose_name = "Экспонат"
        verbose_name_plural = "Экспонаты"
        ordering = ("-year", "name")

    def __str__(self):
        return self.name

    def calculate_age(self):
        from datetime import datetime
        return datetime.now().year - self.year

    def get_status(self):
        if self.condition:
            return self.condition.get_status(self.is_available)
        if not self.is_available:
            return "Недоступен"
        return "Доступен"

    def get_absolute_url(self):
        return reverse("exhibits:detail", kwargs={"exhibit_id": self.pk})