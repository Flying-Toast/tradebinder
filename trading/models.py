from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import cards.models


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    binder = models.OneToOneField("Binder", on_delete=models.CASCADE)


class Binder(models.Model):
    pass


class Have(models.Model):
    binder = models.ForeignKey(Binder, on_delete=models.CASCADE)
    card = models.ForeignKey(cards.models.Card, on_delete=models.CASCADE)


class Want(models.Model):
    binder = models.ForeignKey(Binder, on_delete=models.CASCADE)
