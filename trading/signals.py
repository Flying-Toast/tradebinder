from django.dispatch import receiver
from django.db.models.signals import post_save
from . import models


@receiver(post_save, sender=models.User)
def make_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        profile = models.UserProfile(
            user=instance,
            binder=models.Binder(),
        )
        profile.save()
