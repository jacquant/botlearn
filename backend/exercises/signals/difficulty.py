from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.difficulty import Difficulty


def empty_cache():
    cache.delete("difficulties_all")


@receiver(post_save, sender=Difficulty)
def difficulty_saved(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a difficulty
    """
    empty_cache()


@receiver(post_delete, sender=Difficulty)
def difficulty_deleted(sender, instance, created, *args, **kwargs):
    """
    Handles the remove of a difficulty
    """
    empty_cache()
