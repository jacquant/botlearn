from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.target_students import TargetStudents


def empty_cache():
    """Delete the cache for the TargetStudents objects."""
    cache.delete("target_students_all")


@receiver(post_save, sender=TargetStudents)
def target_students_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a target students."""
    empty_cache()


@receiver(post_delete, sender=TargetStudents)
def target_students_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a target students."""
    empty_cache()
