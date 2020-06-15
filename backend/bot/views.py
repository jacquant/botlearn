from celery import shared_task
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.ext.django_chatterbot import settings
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import (
    ListTrainer,
)
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import F
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.models import (
    Question,
)
from bot.serializers import QuestionSerializer
from bot.trainer import train_bot
from exercises.models.exercise import Exercise
from memoire import settings as default_settings

CACHE_TTL = getattr(default_settings, "CACHE_TTL", DEFAULT_TIMEOUT)

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


def format_exercise(exercise):
    """Format an exercise object with html."""
    return '<a href="{0}media/{1}" target="_blank" id={4}>{2} (à rendre pour le {3})</a>'.format(
        default_settings.BACK_URL,
        exercise.project_files,
        exercise.name,
        exercise.due_date,
        exercise.id,
    )


def get_exercises():
    """Return all the future exercises to the api in html format."""
    key = "exercises_all"
    if key in cache:
        exercises = cache.get(key)
    else:
        exercises = Exercise.objects.all()
        cache.set(key, exercises, timeout=CACHE_TTL)
    exercises = exercises.filter(due_date__gte=timezone.now())
    if exercises:
        return "<p>Oui ! La voici!</p><br>" + "<br>".join(format_exercise(exercise) for exercise in exercises)
    return "{0}{1}".format(
        "<h5 style='color:red;'>Aucun",
        " exercice disponible pour le moment.</h5>",
    )


@shared_task
def update_question(answer, question_text):
    """Update question database."""
    if "<p>Désolé mais je n'ai pas compris la question" in answer:
        key = "questions_all"
        if key in cache:
            questions = cache.get(key)
        else:
            questions = Question.objects.all()
            cache.set(key, questions, timeout=CACHE_TTL)
        question, created = questions.get_or_create(title=question_text)
        if not created:
            question.asked = F("asked") + 1
            question.save(update_fields=["asked"])
    # Update the number question asked
    else:
        text = Statement(question_text)

        search_results = chatterbot.search_algorithms[
            "indexed_text_search"
        ].search(text)

        current_similarity = 0
        closest_match = ""
        for result in search_results:
            # update
            if result.confidence >= current_similarity:
                closest_match = result
                current_similarity = result.confidence
        if closest_match != "":
            question, created = Question.objects.get_or_create(title=closest_match)
            question.asked = F("asked") + 1
            question.save(update_fields=["asked"])


class AnswerViewSet(APIView):
    """API view to request question with the Bot."""
    permission_classes = [permissions.IsAuthenticated]

    # Defined and train the bot

    @swagger_auto_schema(request_body=QuestionSerializer)
    def post(self, request, *args, **kwargs):
        """Provides a method to send a message to the bot an get an answer.
        # Request: POST
        ## Parameters
        None
        ## Permissions
        ### Token: Bearer
        - The user must be **authenticated**, so the given token must be valid
        ## Return
        - The return is a message in string include in a JSON
        """
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if "liste des exercices" in serializer.validated_data["text"]:
            response_content = QuestionSerializer(data={"text": get_exercises()})
        else:
            answer = chatterbot.get_response(serializer.validated_data)
            response_content = QuestionSerializer(data={"text": answer.text})
            # Save question if no answer => Better way to do it ?
            update_question.delay(answer.text, serializer.validated_data["text"])
        if response_content.is_valid():
            return Response(response_content.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(response_content.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrainingBot(APIView):
    """Api View to train the bot."""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        """An Api View which provides a method to train the chatbot.
        # Request: GET
        ## Parameters
        None
        ## Permissions
        ### Token: Bearer
        - The user must be **authenticated**, so the given token must be valid
        ## Return
        - The return is a message in string include in a JSON
        """
        chatterbot.storage.drop()

        # Training based on corpus (YML)
        # trainer_corpus = ChatterBotCorpusTrainer(self.chatterbot)
        # trainer_corpus.train("chatterbot.corpus.french")

        # Training based on question written by the admin panel
        trainer_own = ListTrainer(chatterbot)
        train_bot(trainer_own)

        return Response({"text": "done"}, status=status.HTTP_200_OK)
