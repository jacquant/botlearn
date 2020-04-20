from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.category import Category


@shared_task
def empty_cache():
    """Delete the cache for all Category objects."""
    cache.delete("categories_all")


@receiver(post_save, sender=Category)
def category_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a category."""
    empty_cache.delay()


@receiver(post_delete, sender=Category)
def category_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a category."""
    empty_cache.delay()
