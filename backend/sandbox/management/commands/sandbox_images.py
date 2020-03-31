import os
import pathlib

import docker
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create linter and formater docker images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-cache", action="store_true", help="Do not use cache to build images",
        )

    def handle(self, *args, **options):
        client = docker.from_env()
        path = os.path.join(pathlib.Path(__file__).parent.absolute(), "Docker")
        for my_image in [
            ["epicbox-linter", "LinterDockerfile"],
            ["epicbox-formatter", "FormatterDockerfile"],
        ]:
            if options["no_cache"]:
                no_caching = True
            else:
                no_caching = False
            image = client.images.build(
                tag=my_image[0], path=path, dockerfile=my_image[1], rm=True, forcerm=True, nocache=no_caching,
            )
            self.print_logs_build(image[1])

    def print_logs_build(self, streamer):
        for chunk in streamer:
            if "stream" in chunk:
                for line in chunk["stream"].splitlines():
                    self.stdout.write(line)
