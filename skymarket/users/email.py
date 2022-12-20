from django.contrib.auth.tokens import default_token_generator
from djoser import email
from djoser import utils
from djoser.conf import settings


class UserPasswordResetEmail(email.PasswordResetEmail):
    """
    Сброс и восстановление пароля через почту
    """

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = "localhost:3000"

        return context
