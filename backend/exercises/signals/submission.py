from django.core.cache import cache
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from exercises.models.submission import Submission


def empty_cache():
    """Delete the cache for the Submission objects."""
    cache.delete("submissions_all")


@receiver(post_save, sender=Submission)
def submission_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a submission."""
    empty_cache()


@receiver(post_delete, sender=Submission)
def submission_deleted(sender, instance, *args, **kwargs):
    """Handles the remove of a submission."""
    empty_cache()
