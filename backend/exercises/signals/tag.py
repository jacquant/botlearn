from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.tag import Tag


@receiver(post_save, sender=Tag)
def tag_update(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a user
    """
    cache.delete("tags_all")
