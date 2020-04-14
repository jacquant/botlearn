from django.apps import AppConfig


class SandboxConfig(AppConfig):
    """Sandbox app configuration."""

    name = "sandbox"

    def ready(self):
        """Method run when the app is ready.

        Launch the signals handlers.
        """
        from sandbox.docker_profiles import configure_docker

        configure_docker()
