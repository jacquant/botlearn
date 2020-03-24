import uuid
from pathlib import Path

import docker
from celery import shared_task
from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.template.loader import render_to_string

from exercises.models.exercise import Exercise
from sandbox.models import SandboxProfile


def empty_cache():
    cache.delete("exercises_all")


def create_dockerfile(instance):
    requirements_list = " ".join(
        instance.requirements.all().distinct().values_list("name", flat=True)
    )
    tar_file = "*.tar.gz"
    dockerfile_string = render_to_string(
        "Docker/Dockerfile",
        {
            "tar": True,
            "file_tar": tar_file,
            "requirements": True,
            "requirements_list": requirements_list,
            "requirements_file": False,
        },
    )
    Path(
        "media/exercises/{}/".format(uuid.uuid5(uuid.NAMESPACE_DNS, instance.name))
    ).mkdir(parents=True, exist_ok=True)
    path = "media/exercises/{}/Dockerfile".format(
        uuid.uuid5(uuid.NAMESPACE_DNS, instance.name)
    )
    with open(path, "w") as dockerfile:
        print(dockerfile_string, file=dockerfile)
    path_without_media = path[6:]
    return path_without_media


@shared_task
def create_docker_image(tag_image, dockerfile_dir, id_docker_image):
    client = docker.from_env()
    image_tuple = client.images.build(
        tag=tag_image,
        path=dockerfile_dir,
        dockerfile="Dockerfile",
        rm=True,
        forcerm=True,
    )
    SandboxProfile.objects.filter(id=id_docker_image).update(
        image_id=image_tuple[0].short_id
    )


def build_docker(instance):
    id_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id)))
    path_dockerfile = create_dockerfile(instance)
    docker_image, created = SandboxProfile.objects.update_or_create(
        profile_name=id_uuid,
        image_name="{id}:latest".format(id=id_uuid),
        dockerfile=path_dockerfile,
    )
    Exercise.objects.filter(id=instance.id).update(dockerImage=docker_image)
    dockerfile_dir = "media/exercises/{}/".format(
        uuid.uuid5(uuid.NAMESPACE_DNS, instance.name)
    )
    create_docker_image.delay(id_uuid, dockerfile_dir, docker_image.id)


@receiver(post_save, sender=Exercise)
def exercise_saved(sender, instance, created, *args, **kwargs):
    """
    Handles the save of a exercise
    """
    empty_cache()
    transaction.on_commit(
        lambda: build_docker(instance)
    )  # Wait until the m2m is fully updated


@receiver(post_delete, sender=Exercise)
def exercise_deleted_post(sender, instance, *args, **kwargs):
    """
    Handles the remove of a exercise
    """
    empty_cache()
    if instance.dockerImage:
        instance.dockerImage.delete()
