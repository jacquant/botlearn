import json

from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from exercises.models.exercise import Exercise
from bot.models import Reponse
from exercises.serializers.exercise import ExerciseSerializer

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.ext.django_chatterbot import settings 
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import levenshtein_distance
from chatterbot.response_selection import get_first_response



from datetime import datetime, time

import re


class AnswerViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated]
    # Defined and train the bot
    chatterbot = ChatBot(**settings.CHATTERBOT,
                        read_only=True,
                        response_selection_method=get_first_response,
                        statement_comparison_function=levenshtein_distance,
                        logic_adapters=[{
                            'maximum_similarity_threshold': 0.75,
                            "import_path": "chatterbot.logic.BestMatch",
                            'default_response': 
                            "<p>Désolé mais je n'ai pas compris la question :( Pourrais-tu la reformuler s'il te plait.</p><p> <div style='color:red;'>Attention !</div> Il faut savoir que je réponds aux questions liées à la programmation en générale, pas sur l'exercice.</p>",
                        }])

    def post(self, request, *args, **kwargs):
        """
        An Api View which provides a method to send a message to the bot an get an answer

        # Request: POST

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a message in string include in a JSON

        """
        input_data = json.loads(request.body.decode('utf-8'))
      
        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()
        # Modify data to add exercices if it's requested
        if("liste des exercices" in input_data["text"]):
            response_data["text"] += self.getExercice()

        print("################################################################################")
        return JsonResponse(response_data, status=200)

    def getExercice(self, data=None):
        exercices = Exercise.objects.all()
        serializer = ExerciseSerializer(exercices, many=True)

        # Get Current Time
        now = datetime.now()

        exercices_string = ""
        # print(serializer.data)

        for exercice in serializer.data:
            for info in exercice.items():
                if(info[0] == "name"):
                    name = info[1]
                if(info[0] == "due_date"):
                    time = datetime.strptime(info[1],'%Y-%m-%dT%H:%M:%S%fZ')
                if (info[0] == "project_files"):
                    path = info[1]
                    if (now < time):
                        exercices_string +='- <a href="http://localhost:8080' + str(path) +'">' + name + " (à rendre pour le "+ str(time) + ")</a>" + "<br>"

        # print(exercices_string)
        if (exercices_string == ""):
            exercices_string = "<h5 style='color:red;'>Aucun exercice disponible pour le moment.</h5>"
        return exercices_string


class TrainingBot(APIView):

    chatterbot = AnswerViewSet.chatterbot

    def get(self, request, *args, **kwargs):
        """
        An Api View which provides a method to train the chatbot

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
        trainerCoprus = ChatterBotCorpusTrainer(self.chatterbot)

        trainerCoprus.train('chatterbot.corpus.french')

        # Training based on question written by the admin panel
        trainerOwn = ListTrainer(self.chatterbot)
        for response in Reponse.objects.all():
            for question in response.question.all():
                # Modify the code snippet to HMTL to diplay it correctly in the chatbot
                modify_code = re.sub(r'    ', "&nbsp;&nbsp;&nbsp;&nbsp;", response.reponse)
                modify_code = re.sub(r'(\r\n){1}(?!\r\n)', "<br>", modify_code)
                trainerOwn.train([question.intitule, modify_code])

        return JsonResponse({
            'text': "done"
        })
