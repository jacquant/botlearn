from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.difficulty import Difficulty


@receiver(post_save, sender=Difficulty)
def difficulty_update(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a user
    """
    cache.delete("difficulties_all")
