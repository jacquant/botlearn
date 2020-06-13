from chatterbot.ext.django_chatterbot.models import Statement, Tag
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from import_export.admin import ImportExportModelAdmin

from bot.models import (
    Answer,
    Question,
)
from bot.models import Statement as MyStatement


class AnswerAdmin(ImportExportModelAdmin):
    """Custom answer admin interface class."""

    def save_model(self, request, response_obj, form, change):
        """Override save model to manage the update of questions."""
        try:
            old_values = Answer.objects.get(id=response_obj.id).question.filter()
        except ObjectDoesNotExist:
            old_values = []

        new_values = form.cleaned_data["question"].all()
        elements_removed = [
            old_value
            for old_value in old_values
            if old_value not in new_values
        ]

        # Update questions removed  to False
        for element_removed in elements_removed:
            if len(Answer.objects.filter(question=element_removed)) == 1:
                element_removed.matched = False
                element_removed.save()

        # Update new questions to True
        response_obj.user = request.user
        for que in form.cleaned_data["question"].all():
            que.matched = True
            que.save()

        super().save_model(request, response_obj, form, change)

    search_fields = ("response",)


class QuestionAdmin(ImportExportModelAdmin):
    """Custom question admin interface class."""

    exclude = ("matched",)
    list_display = (
        "title",
        "matched",
        "asked",
    )
    search_fields = ("title",)


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'in_response_to', 'conversation', 'created_at',)
    list_filter = ('text', 'created_at',)
    search_fields = ('text',)


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.unregister(Statement)
admin.site.unregister(Tag)

admin.site.register(MyStatement, StatementAdmin)
