import epicbox
from .models import SandboxProfile


def configure_docker():
    sandboxes = SandboxProfile.objects.all()
    print(sandboxes)
    profiles = [epicbox.Profile(s.profile_name, s.image_name) for s in sandboxes]
    profiles.extend(
        [
            epicbox.Profile("executor", "epicbox-executor:latest"),
            epicbox.Profile("linter", "epicbox-linter:latest"),
            epicbox.Profile("formatter", "epicbox-formatter:latest"),
        ]
    )
    epicbox.configure(profiles=profiles)
