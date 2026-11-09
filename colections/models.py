from django.db import models


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    class Meta:
        db_table = "collections"
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
        ordering = ("name",)

    def __str__(self):
        return self.name