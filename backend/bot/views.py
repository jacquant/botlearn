import json
import re

from django.http import JsonResponse
from django.utils import timezone

from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.conversation import Statement
from chatterbot.ext.django_chatterbot import settings
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import (
    ChatterBotCorpusTrainer,
    ListTrainer,
)
from rest_framework import permissions
from rest_framework.views import APIView

from bot.models import (
    Answer,
    Question,
)
from exercises.models.exercise import Exercise
from memoire.settings import BACK_URL


def format_exercise(exercise):
    """Format an exercise object with html."""
    return '<a href="{0}{1}" target="_blank" id={4}>{2} (à rendre pour le {3})</a><br>'.format(
        BACK_URL,
        exercise.project_files,
        exercise.name,
        exercise.due_date,
        exercise.id,
    )


def get_exercises():
    """Return all the future exercises to the api in html format."""
    exercises = Exercise.objects.filter(due_date__gte=timezone.now())
    if exercises:
        return "".join(format_exercise(exercise) for exercise in exercises)
    return "{0}{1}".format(
        "<h5 style='color:red;'>Aucun",
        " exercice disponible pour le moment.</h5>",
    )


class AnswerViewSet(APIView):
    """API view to request question with the Bot."""

    permission_classes = [permissions.IsAuthenticated]

    # Defined and train the bot
    chatterbot = ChatBot(
        **settings.CHATTERBOT,
        read_only=True,
        response_selection_method=get_first_response,
        statement_comparison_function=levenshtein_distance,
        logic_adapters=[
            {
                "maximum_similarity_threshold": 0.75,
                "import_path": "chatterbot.logic.BestMatch",
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

        input_data = json.loads(request.body.decode("utf-8"))
        if "text" not in input_data:
            return JsonResponse(
                {"text": ['The attribute "text" is required.']}, status=400
            )

        answer = self.chatterbot.get_response(input_data)
        response_data = answer.serialize()
        # Save question if no answer => Better way to do it ?
        self.update_question(answer.text, input_data["text"])

        # Modify data to add exercices if it's requested
        if "liste des exercices" in input_data["text"]:
            response_data["text"] += get_exercises()

        return JsonResponse(response_data, status=200)

    def update_question(self, answer, question):
        """Update question database."""
        if "<p>Désolé mais je n'ai pas compris la question" in answer:
            if Question.objects.filter(title=question).first() is not None:
                question = Question.objects.filter(title=question).first()
                question.asked += 1
                question.save()
            else:
                Question.objects.create(title=question, matched=False)
        # Update the number question asked
        else:
            text = Statement(question)

            search_results = self.chatterbot.search_algorithms[
                "indexed_text_search"
            ].search(text)
            
            current_similarity = 0
            for result in search_results:
                # update
                if result.confidence >= current_similarity:
                    closest_match = result
                    current_similarity = result.confidence
            # question = Question.objects.filter(title=closest_match).first()
            # question.asked += 1
            # question.save()


class TrainingBot(APIView):
    """Api View to train the bot."""

    chatterbot = AnswerViewSet.chatterbot

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
        self.chatterbot.storage.drop()

        # Training based on corpus (YML)
        trainer_corpus = ChatterBotCorpusTrainer(self.chatterbot)
        trainer_corpus.train("chatterbot.corpus.french")

        # Training based on question written by the admin panel
        trainer_own = ListTrainer(self.chatterbot)
        for answer in Answer.objects.all():
            # Modify the code snippet to HMTL to diplay it correctly in the
            # chatbot
            modify_code = re.sub(
                r" {4}", "&nbsp;&nbsp;&nbsp;&nbsp;", answer.answer
            )
            modify_code = re.sub(r"(\r\n){1}(?!\r\n)", "<br>", modify_code)
            for question in answer.question.all():
                trainer_own.train([question.title, modify_code])

        return JsonResponse({"text": "done"})
