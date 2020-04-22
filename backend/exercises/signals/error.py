from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.error import Error


@shared_task
def empty_cache():
    """Delete the cache for all Error objects."""
    cache.delete("errors_all")


@receiver(post_save, sender=Error)
def error_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a error."""
    empty_cache.delay()


@receiver(post_delete, sender=Error)
def error_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a error."""
    empty_cache.delay()
