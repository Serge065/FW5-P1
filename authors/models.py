from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Имя")
    lastname = models.CharField(max_length=100, verbose_name="Фамилия")

    class Meta:
        db_table = "authors"
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("lastname", "name")

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.name} {self.lastname}"