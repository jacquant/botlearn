"""Module to manage signals and tasks related to sandbox."""
from celery import shared_task
from django.db.models.signals import pre_delete
from django.dispatch import receiver

import docker

from sandbox.models import SandboxProfile


@shared_task
def remove_docker_image(id_image):
    """Remove a docker image.

    :param id_image: the id of the docker image
    :type id_image: str
    """
    client = docker.from_env()
    client.images.remove(image=id_image)


@receiver(pre_delete, sender=SandboxProfile)
def sandbox_deleted_pre(sender, instance, *args, **kwargs):
    """Catch signal before SandboxProfile."""
    if instance.image_id:
        remove_docker_image.delay(instance.image_id)
