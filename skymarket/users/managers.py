from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """
    Функция создания пользователя. В нее мы передаем обязательные поля
    """

    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.role = "user"
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        """
        Функция для создания суперпользователя. С ее помощью мы создаем администратора.
        Это можно сделать с помощью команды createsuperuser
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.role = "admin"
        user.save(using=self._db)

        return user
