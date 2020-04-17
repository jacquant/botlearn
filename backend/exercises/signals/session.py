from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.session import Session


@shared_task
def empty_cache():
    """Delete the cache for the Session objects."""
    cache.delete("sessions")


@receiver(post_save, sender=Session)
def session_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a session."""
    empty_cache.delay()


@receiver(post_delete, sender=Session)
def session_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a session."""
    empty_cache.delay()
