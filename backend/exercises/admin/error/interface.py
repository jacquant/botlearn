from import_export.admin import ImportExportModelAdmin

from exercises.admin.error.resource import ErrorResource


class ErrorAdmin(ImportExportModelAdmin):
    """Admin interface for the Error model."""

    resource_class = ErrorResource
