import uuid
from pathlib import Path

from celery import shared_task
from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import (
    post_delete,
    post_save, pre_save,
)
from django.dispatch import receiver
from django.template.loader import render_to_string

import docker
import tarfile
from exercises.models.exercise import Exercise
from sandbox.models import SandboxProfile


@shared_task
def empty_cache():
    """Function to delete the cache for all Exercise objects."""
    cache.delete("exercises_all")


def check_requirements_file(name_uuid):
    try:
        with tarfile.open("media/exercises/{0}/archive.tar.gz".format(name_uuid), "r:gz") as f:
            if "requirements.txt" in f.getnames():
                return True
            else:
                return False
    except FileNotFoundError:
        return False


def create_dockerfile(instance, name_uuid):
    """Create and render a Dockerfile with needed element from the Exercise."""
    requirements_list = " ".join(
        instance.requirements.all().distinct().values_list("name", flat=True),
    )
    if len(requirements_list) == 0:
        requirements = False
    else:
        requirements = True

    requirement_files = check_requirements_file(name_uuid)
    if instance.project_files.name == "":
        tar = False
    else:
        tar = True
    dockerfile_string = render_to_string(
        "Docker/Dockerfile",
        {
            "tar": tar,
            "file_tar": "*.tar.gz",
            "requirements": requirements,
            "requirements_list": requirements_list,
            "requirements_file": requirement_files,
        },
    )
    Path("media/exercises/{0}/".format(name_uuid)).mkdir(
        parents=True, exist_ok=True
    )
    path = "media/exercises/{0}/Dockerfile".format(name_uuid)
    with open(path, "w") as dockerfile:
        print(dockerfile_string, file=dockerfile)  # noqa: WPS421
    return path[6:]  # Removed media


@shared_task
def create_docker_image(tag_image, dockerfile_dir, id_docker_image):
    """Create a tagged docker image."""
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
    """Build a docker for a specific exercise object.

    Modify the instance(trick filter+update==> no signal sent).
    """
    id_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id)))
    name_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, instance.name))
    path_dockerfile = create_dockerfile(instance, name_uuid)
    docker_image, _created = SandboxProfile.objects.update_or_create(
        profile_name=id_uuid,
        image_name="{id}:latest".format(id=id_uuid),
        dockerfile=path_dockerfile,
    )
    Exercise.objects.filter(id=instance.id).update(docker_image=docker_image)
    create_docker_image.delay(
        id_uuid, "media/exercises/{0}/".format(name_uuid), docker_image.id
    )


@receiver(pre_save, sender=Exercise)
def exercise_will_be_saved(sender, instance, *args, **kwargs):
    exercise = Exercise.objects.get(id=instance.id)
    if exercise.project_files != "":
        if instance.project_files == "":
            exercise.project_files.delete(False)


@receiver(post_save, sender=Exercise)
def exercise_saved(sender, instance, created, *args, **kwargs):
    """Handles the save of a exercise."""
    empty_cache.delay()
    # Wait until the m2m is fully updated
    transaction.on_commit(lambda: build_docker(instance))


@receiver(post_delete, sender=Exercise)
def exercise_deleted_post(sender, instance, *args, **kwargs):
    """Handles the remove of a exercise."""
    empty_cache.delay()
    if instance.docker_image:
        instance.docker_image.delete()
