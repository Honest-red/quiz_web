from django.apps import AppConfig
from django.dispatch import Signal

from .utils import send_activation_notification


user_registered = Signal()
user_raiting = Signal()


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


def user_raiting_dispatcher(sender, **kwargs):
    user = kwargs['instance']
    user.raiting += int(sender)
    user.save()


user_raiting.connect(user_raiting_dispatcher)
user_registered.connect(user_registered_dispatcher)
