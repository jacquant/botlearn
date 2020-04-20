from import_export import resources

from exercises.models.error import Error


class ErrorResource(resources.ModelResource):
    """Resource used for import and export Error objects from/to files."""

    class Meta(object):
        """Meta class to define the fields used."""

        model = Error
