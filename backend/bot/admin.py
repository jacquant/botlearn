from django.contrib import admin
from bot.models import Question, Reponse


@admin.register(Reponse)
class ResponseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        for que in form.cleaned_data['question'].all():
            que.matched = True
            que.save()

        super().save_model(request, obj, form, change)


admin.site.register(Question)
