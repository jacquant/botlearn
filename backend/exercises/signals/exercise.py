from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.exercise import Exercise


@receiver(post_save, sender=Exercise)
def exercise_update(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a user
    """
    cache.delete("exercises_all")
    cache.delete_pattern("exercises_session_id_*")
    cache.delete_pattern("exercises_section_id_*")