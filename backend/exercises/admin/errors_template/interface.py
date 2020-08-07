from import_export.admin import ImportExportModelAdmin

from exercises.admin.errors_template.resource import ErrorsTemplateResource


class ErrorsTemplateAdmin(ImportExportModelAdmin):
    """Admin interface for the ErrorsTemplate model."""

    resource_class = ErrorsTemplateResource
