from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from bot.models import Question, Reponse


@admin.register(Reponse)
class ResponseAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        try:
            old_values = Reponse.objects.get(id=obj.id).question.filter()
        except ObjectDoesNotExist:
            old_values = []
        
        new_values = form.cleaned_data['question'].all()
        elements_removed = [x for x in old_values if x not in new_values]

        # Update questions removed  to False
        for data in elements_removed:
            if len(Reponse.objects.filter(question=data)) == 1:
                data.matched = False
                data.save()

        # Update new questions to True
        obj.user = request.user
        for que in form.cleaned_data['question'].all():
            que.matched = True
            que.save()

        super().save_model(request, obj, form, change)

    search_fields = (
        'reponse',
        )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    exclude = ('matched',)
    list_display = ('intitule', 'matched', 'asked',)
    search_fields = (
        'intitule',
        )
    