from datetime import date
from django.db import models
from django.contrib.auth.models import User

# class Genre(models.Model):
#     name = models.CharField("Тип", max_length=128)
#     url = models.SlugField(max_length=256, unique=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Тип"
#         verbose_name_plural = "Типы"


class Food(models.Model):
    name = models.CharField('Название выпечки', max_length=64)
    image = models.ImageField('Фото выпечки', upload_to='bakerser/')
    composition = models.TextField('Состав выпечки')
    description = models.TextField('Описание выпечки')
    # genres = models.ManyToManyField(Genre, verbose_name="Типы")
    pub_date = models.DateField('Дата создания выпечки', default=date.today)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Выпечку'
        verbose_name_plural = 'Выпечка'

class RatingStar(models.Model):
    value = models.SmallIntegerField("Значиние", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        verbose_name="фильм",
        related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.food}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Comment(models.Model):
    author = models.CharField(verbose_name='Автор комментария', max_length=128, default='')
    comment_text = models.CharField('Текст комментария', max_length=256)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, default='')

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


