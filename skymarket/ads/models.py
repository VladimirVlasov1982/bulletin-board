from datetime import datetime
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ad(models.Model):
    """
    Модель объявления
    """
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Цена")
    description = models.CharField(max_length=1500, verbose_name="Описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads", verbose_name="Владелец")
    created_at = models.DateTimeField(default=datetime.now(), verbose_name="Создано")
    image = models.ImageField(upload_to="ads_image/", null=True, verbose_name="Картинка")

    objects = models.Manager()

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель отзыва
    """
    text = models.CharField(max_length=400, verbose_name="Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Объявление")
    created_at = models.DateTimeField(default=datetime.now(), verbose_name="Создано")

    objects = models.Manager()

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text
