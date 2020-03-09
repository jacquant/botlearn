from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.session import Session


def empty_cache():
    cache.delete("sessions")


@receiver(post_save, sender=Session)
def session_saved(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a session
    """
    empty_cache()


@receiver(post_delete, sender=Session)
def session_deleted(sender, instance, *args, **kwargs):
    """
    Handles the remove of a session
    """
    empty_cache()
