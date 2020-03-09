from django.db.models.signals import pre_delete
from django.dispatch import receiver
import docker
from celery import shared_task
from .models import SandboxProfile


@shared_task
def remove_docker_image(id_image):
    client = docker.from_env()
    client.images.remove(image=id_image)
    print("done")


@receiver(pre_delete, sender=SandboxProfile)
def sandbox_deleted_pre(sender, instance, *args, **kwargs):
    remove_docker_image.delay(instance.image_name)
