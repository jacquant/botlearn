from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.section import Section


@receiver(post_save, sender=Section)
def section_update(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a user
    """
    cache.delete("sections_all")
