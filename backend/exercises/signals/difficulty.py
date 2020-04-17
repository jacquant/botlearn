from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.difficulty import Difficulty


@shared_task
def empty_cache():
    """Delete the cache for all Difficulty objects."""
    cache.delete("difficulties_all")


@receiver(post_save, sender=Difficulty)
def difficulty_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a difficulty."""
    empty_cache.delay()


@receiver(post_delete, sender=Difficulty)
def difficulty_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a difficulty."""
    empty_cache.delay()
