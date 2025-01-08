from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_profile_with_new_user(sender, instance, created, raw, **kwargs):
    if created and not raw:
        Profile.objects.create(user=instance)
