from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.error_count import ErrorCount


@shared_task
def empty_cache():
    """Delete the cache for all ErrorCount objects."""
    cache.delete("errors_count_all")


@receiver(post_save, sender=ErrorCount)
def error_count_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a error_count."""
    empty_cache.delay()


@receiver(post_delete, sender=ErrorCount)
def error_count_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a error_count."""
    empty_cache.delay()
