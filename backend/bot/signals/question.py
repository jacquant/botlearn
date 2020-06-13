from celery import shared_task
from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from bot.models import Question


@shared_task
def empty_cache():
    """Delete the cache for all Question objects."""
    cache.delete("questions_all")


@receiver(post_save, sender=Question)
def question_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a question."""
    empty_cache.delay()


@receiver(post_delete, sender=Question)
def question_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a question."""
    empty_cache.delay()
