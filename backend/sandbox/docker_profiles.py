import epicbox


def configure_docker():
    """Function used to configure base profile."""
    profiles = [
        epicbox.Profile("linter", "epicbox-linter:latest"),
        epicbox.Profile("formatter", "epicbox-formatter:latest"),
    ]
    epicbox.configure(profiles=profiles)
