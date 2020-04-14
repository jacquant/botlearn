from django.contrib import admin

from bot.models import (
    Answer,
    Question,
)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Custom answer admin interface class."""

    def save_model(self, request, response_obj, form, change):
        """Override save model to manage the update of questions."""
        old_values = Answer.objects.get(id=response_obj.id).question.filter()
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


class QuestionAdmin(admin.ModelAdmin):
    """Custom question admin interface class."""

    exclude = ("matched",)
    list_display = (
        "intitule",
        "matched",
        "asked",
    )
    search_fields = ("intitule",)


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
