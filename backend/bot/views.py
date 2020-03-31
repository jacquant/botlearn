import json
from datetime import datetime

from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.ext.django_chatterbot import settings
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView

from exercises.models.exercise import Exercise
from exercises.serializers.exercise import ExerciseSerializer


class AnswerViewSet(APIView):

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
                "default_response": "<p>Désolé mais je n'ai pas compris la question :( Pourrais-tu la reformuler s'il "
                "te plait.</p><p> <div style='color:red;'>Attention !</div> Il faut savoir que je "
                "réponds aux questions liées à la programmation en générale, "
                "pas sur l'exercice.</p>",
            }
        ]
    )

    # Delete Storage
    # chatterbot.storage.drop()

    # Corpus Part
    trainerCoprus = ChatterBotCorpusTrainer(chatterbot)

    trainerCoprus.train("chatterbot.corpus.french")

    # trainerOwn.train("./files/")

    # Own training
    trainerOwn = ListTrainer(chatterbot)

    def post(self, request, *args, **kwargs):
        """
        An Api View which provides a method to send a message to the bot an get an answer

        # Request: POST

        ## Parameters

        None

        ### Query parameters

        - difficulty_id: the id of the difficulty

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a message in string include in a JSON

        """
        print("################################################################################")
        # self.trainMyBot(self.chatterbot)

        input_data = json.loads(request.body.decode("utf-8"))

        if "text" not in input_data:
            return JsonResponse({"text": ['The attribute "text" is required.']}, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()
        # Modify data to add exercices if it's requested
        if "liste des exercices" in input_data["text"]:
            response_data["text"] += self.get_exercice()

        print("################################################################################")
        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({"name": self.chatterbot.name})

    def get_exercice(self, data=None):
        exercices = Exercise.objects.all()
        serializer = ExerciseSerializer(exercices, many=True)

        # Get Current Time
        now = datetime.now()

        exercices_string = ""
        # print(serializer.data)

        for exercice in serializer.data:
            for info in exercice.items():
                if info[0] == "name":
                    name = info[1]
                if info[0] == "due_date":
                    time = datetime.strptime(info[1], "%Y-%m-%dT%H:%M:%S%fZ")
                if info[0] == "project_files":
                    path = info[1]
                    if now < time:
                        exercices_string += (
                            '- <a href="http://localhost:8080'
                            + str(path)
                            + '">'
                            + name
                            + " (à rendre pour le "
                            + str(time)
                            + ")</a>"
                            + "<br>"
                        )

        # print(exercices_string)
        if exercices_string == "":
            exercices_string = "<h5 style='color:red;'>Aucun exercice disponible pour le moment.</h5>"
        return exercices_string

    def trainMyBot(self, chatterbot):
        chatterbot.storage.drop()

        # Corpus Part
        trainerCoprus = ChatterBotCorpusTrainer(chatterbot)

        trainerCoprus.train("chatterbot.corpus.french")

        # trainerOwn.train("./files/")

        # Own training
        trainerOwn = ListTrainer(chatterbot)

        # Getting Help
        """trainerOwn.train([
            "j'ai besoin d'aide s'il te plait !",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

        trainerOwn.train([
            "aide moi",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

        trainerOwn.train([
            "je peux avoir de l'aide ?",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

        trainerOwn.train([
            "tu saurais m'aider ?",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

        """  # Problem With loop
        """
        trainerOwn.train([
            "J'ai un problème avec ma boucle.",
            "Tu utilises une boucle 'for' ou une boucle 'while' ?",
            "une boucle for.",
            "Merci pour l'info ! Donne moi plus d'infos sur ton erreur s'il te plait."
        ])

        trainerOwn.train([
            "J'ai un problème avec ma boucle.",
            "Tu utilises une boucle 'for' ou une boucle 'while' ?",
            "une boucle while.",
            "Merci pour l'info ! Donne moi plus d'infos sur ton erreur s'il te plait."
        ])

        trainerOwn.train([
            "Ma boucle ne fonctionne pas.",
            "Explique-moi ce qu'il se passe avec ta boucle s'il te plait.",
        ])

        trainerOwn.train([
            "Ma boucle for ne fonctionne pas.",
            "Pourquoi cela ne fonctionne pas ? Détails-moi ton erreur.",
        ])

        trainerOwn.train([
            "Ma boucle while ne fonctionne pas.",
            "On va regarder ça ensemble, explique moi en détails ce qu'il se passe.",
        ])"""

        # Getting Exercices
        trainerOwn.train(["Je peux avoir la liste des exercices", "Oui ! La voici: <br>"])
