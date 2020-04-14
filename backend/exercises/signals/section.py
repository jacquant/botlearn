from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.section import Section


def empty_cache():
    """Delete the cache for the Section objects."""
    cache.delete("sections_all")


@receiver(post_save, sender=Section)
def section_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a section."""
    empty_cache()


@receiver(post_delete, sender=Section)
def section_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a section."""
    empty_cache()
