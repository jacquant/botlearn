from django.apps import AppConfig


class SandboxConfig(AppConfig):
    name = "sandbox"

    def ready(self):
        from sandbox.docker_profiles import configure_docker

        # configure_docker()
        from .signals import sandbox_deleted_pre
