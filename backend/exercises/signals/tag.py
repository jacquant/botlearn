from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.tag import Tag


def empty_cache():
    cache.delete("tags_all")


@receiver(post_save, sender=Tag)
def tag_saved(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a tag
    """
    empty_cache()


@receiver(post_delete, sender=Tag)
def tag_deleted(sender, instance, *args, **kwargs):
    """
    Handles the remove of a tag
    """
    empty_cache()
