from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import MyUserManager


class UserRoles:
    """
    Роли пользователя
    """
    USER = "user"
    ADMIN = "admin"
    choices = ((USER, USER), (ADMIN, ADMIN))


class User(AbstractBaseUser):
    """
    Модель пользователя
    """
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия"
    )
    phone = PhoneNumberField(
        null=False,
        blank=False,
        verbose_name="Номер телефона"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта"
    )
    role = models.CharField(
        max_length=5,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name="Роль пользователя"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Аккаунт активен"
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        default="images/12345.jpg"
    )

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
