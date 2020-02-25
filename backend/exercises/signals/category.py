from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.category import Category


@receiver(post_save, sender=Category)
def category_update(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a user
    """
    cache.delete("categories_all")
