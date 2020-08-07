from celery import shared_task
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.ext.django_chatterbot.models import Statement, Tag
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import ListTrainer
from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from import_export.admin import ImportExportModelAdmin

from bot.models import (
    Answer,
    Question,
)
from bot.models import Statement as MyStatement
from bot.trainer import train_bot


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all())

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["questions"].initial = self.instance.question_set.all()
            self.fields["questions"].widget.attrs['readonly'] = True

    def save(self, *args, **kwargs):
        instance = super(AnswerForm, self).save(commit=False)
        self.fields["questions"].initial.update(answer=None)
        self.cleaned_data["questions"].update(answer=instance)
        return instance


@shared_task
def async_train_bot():
    chatterbot = ChatBot(
        **settings.CHATTERBOT,
        read_only=True,
        response_selection_method=get_first_response,
        logic_adapters=[
            {
                "maximum_similarity_threshold": 0.75,
                "import_path": "bot.chatterbot.OurBestMatch",
                "default_response": (
                    "<p>Désolé mais je n'ai pas compris la question "
                    ":( Pourrais-tu la reformuler s'il te plait."
                    "</p><p><div style='color:red;'>Attention !"
                    "</div> Il faut savoir que je réponds aux questions liées"
                    "à la programmation en générale, pas sur l'exercice.</p>",
                ),
            }
        ],
    )
    chatterbot.storage.drop()

    # Training based on corpus (YML)

    # Training based on question written by the admin panel
    trainer_own = ListTrainer(chatterbot)
    train_bot(trainer_own)


class QuestionInline(admin.StackedInline):
    model = Question


class AnswerAdmin(ImportExportModelAdmin):
    """Custom answer admin interface class."""

    search_fields = ("answer",)
    change_list_template = "admin/changelist.html"
    form = AnswerForm
    inlines = [QuestionInline]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("train/", self.train_bot)
        ]
        return my_urls + urls

    def train_bot(self, request):
        async_train_bot.delay()
        self.message_user(request, "Le bot est maintenant entraîné")
        return HttpResponseRedirect("../")


class QuestionAdmin(ImportExportModelAdmin):
    """Custom question admin interface class."""

    list_display = (
        "title",
        "matched",
        "asked",
    )
    search_fields = ("title",)
    change_list_template = "admin/changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("train/", self.train_bot)
        ]
        return my_urls + urls

    def train_bot(self, request):
        async_train_bot.delay()
        self.message_user(request, "Le bot est maintenant entraîné")
        return HttpResponseRedirect("../")


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'in_response_to', 'conversation', 'created_at',)
    list_filter = ('text', 'created_at',)
    search_fields = ('text',)


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.unregister(Statement)
admin.site.unregister(Tag)

# admin.site.register(MyStatement, StatementAdmin)
