from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.category import Category


def empty_cache():
    cache.delete("categories_all")


@receiver(post_save, sender=Category)
def category_saved(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a category
    """
    empty_cache()


@receiver(post_delete, sender=Category)
def category_deleted(sender, instance, created, *args, **kwargs):
    """
    Handles the remove of a category
    """
    empty_cache()
