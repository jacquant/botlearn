from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.ext.django_chatterbot.models import Statement, Tag
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import ListTrainer
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from celery import shared_task
from bot.models import (
    Answer,
    Question,
)
from bot.models import Statement as MyStatement
from bot.trainer import train_bot


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
    # trainer_corpus = ChatterBotCorpusTrainer(self.chatterbot)
    # trainer_corpus.train("chatterbot.corpus.french")

    # Training based on question written by the admin panel
    trainer_own = ListTrainer(chatterbot)
    train_bot(trainer_own)


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


class AnswerInline(admin.StackedInline):
    model = Answer.question.through


class QuestionAdmin(ImportExportModelAdmin):
    """Custom question admin interface class."""

    exclude = ("matched",)
    list_display = (
        "title",
        "matched",
        "asked",
    )
    search_fields = ("title",)
    change_list_template = "admin/changelist.html"
    inlines = [AnswerInline]

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

admin.site.register(MyStatement, StatementAdmin)
