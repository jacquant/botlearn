from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.session import Session


@receiver(post_save, sender=Session)
def session_update(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a user
    """
    cache.delete("sessions_all")
