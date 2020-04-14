import os
import pathlib

from django.core.management.base import BaseCommand

import docker


class Command(BaseCommand):
    """Command to handle the creation of base sandbox docker images."""

    help = "Create linter and formater docker images"  # noqa: WPS125

    def add_arguments(self, parser):
        """Method to add arguments to the command."""
        parser.add_argument(
            "--no-cache",
            action="store_true",
            help="Do not use cache to build images",
        )

    def handle(self, *args, **options):  # noqa: WPS110
        """Method to handle the command."""
        client = docker.from_env()
        path = os.path.join(pathlib.Path(__file__).parent.absolute(), "Docker")
        images = [
            ["epicbox-linter", "LinterDockerfile"],
            ["epicbox-formatter", "FormatterDockerfile"],
        ]
        for my_image in images:
            image = client.images.build(
                tag=my_image[0],
                path=path,
                dockerfile=my_image[1],
                rm=True,
                forcerm=True,
                nocache=options["no_cache"],
            )
            self.print_logs_build(image[1])

    def print_logs_build(self, streamer):
        """Print the logs of the image build."""
        for chunk in streamer:
            if "stream" in chunk:
                for line in chunk.get("stream").splitlines():
                    self.stdout.write(line)
