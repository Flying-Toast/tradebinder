from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import cards.models


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    binder = models.OneToOneField("Binder", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s profile"


class Binder(models.Model):
    def __str__(self):
        return f"{self.userprofile.user}'s trade binder"


class Have(models.Model):
    binder = models.ForeignKey(Binder, on_delete=models.CASCADE)
    card = models.ForeignKey(cards.models.Card, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.card)


class Want(models.Model):
    binder = models.ForeignKey(Binder, on_delete=models.CASCADE)
    oracle_id = models.UUIDField()
    set = models.ForeignKey(cards.models.Set, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return cards.models.Card.objects.filter(oracle_id=self.oracle_id)[0].name
