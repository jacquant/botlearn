from import_export import resources

from exercises.models.errors_template import ErrorsTemplate


class ErrorsTemplateResource(resources.ModelResource):
    """Resource used for import and export ErrorsTemplate objects from/to files."""

    class Meta(object):
        """Meta class to define the fields used."""

        model = ErrorsTemplate
