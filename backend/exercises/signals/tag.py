from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.tag import Tag


@shared_task
def empty_cache():
    """Delete the cache for the Tag objects."""
    cache.delete("tags_all")


@receiver(post_save, sender=Tag)
def tag_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a tag."""
    empty_cache.delay()


@receiver(post_delete, sender=Tag)
def tag_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a tag."""
    empty_cache.delay()
