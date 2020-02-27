from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.exercise import Exercise


def empty_cache():
    cache.delete_pattern("exercises_*")


@receiver(post_save, sender=Exercise)
def exercise_saved(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a exercise
    """
    empty_cache()


@receiver(post_delete, sender=Exercise)
def exercise_deleted(sender, instance, created, *args, **kwargs):
    """
    Handles the remove of a exercise
    """
    empty_cache()
