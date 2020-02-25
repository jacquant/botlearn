from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from exercises.models.target_students import TargetStudents


@receiver(post_save, sender=TargetStudents)
def target_students_update(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a user
    """
    cache.delete("target_students_all")
