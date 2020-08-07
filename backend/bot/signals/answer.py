from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save
)
from django.dispatch import receiver

from bot.models import Answer


@shared_task
def empty_cache():
    """Delete the cache for all Answer objects."""
    cache.delete("answers_all")


@receiver(post_save, sender=Answer)
def answer_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a answer."""
    empty_cache.delay()


@receiver(post_delete, sender=Answer)
def answer_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a answer."""
    empty_cache.delay()
