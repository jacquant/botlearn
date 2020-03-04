import json

from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from exercises.models.exercise import Exercise
from exercises.serializers.exercise import ExerciseSerializer

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.ext.django_chatterbot import settings 
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.ext.django_chatterbot import settings


class AnswerViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated]
    #Defined and train the bot
    chatterbot = ChatBot(**settings.CHATTERBOT,
                        read_only=True,
                        logic_adapters=[{
                            'import_path': "chatterbot.logic.BestMatch",
                            'default_response': "Désolé mais je n'ai pas compris la question :( Pourrais-tu la reformuler s'il te plait.",
                        }])

    #chatterbot.trainer.export_for_training('./files/programmation.yml')

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
        self.trainMyBot(self.chatterbot)

        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        print("################################################################################")
        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })

    """test post fait maison
    print("##########################################")
    #serializer_class = ProductSerializer

    def post(self, request):
        content = {"message": "Je n'ai pas compris ton message :( Pourrais-tu reformuler différement s'il te plait ?"}

        data = request.data["message"]
        array_data = data.split("%")

        #Understand what the user is saying
        response = None
        specific_data = None

        response = self.needHelp(array_data)

        #specific_data = self.getExercice(data).data

        if (response != None):
            content["message"] = response
        content["data"] = specific_data

        return Response(content)"""

    def needHelp(self, data):
        a_set = set(["aide","aider","besoin d'aide","help"]) 
        b_set = set(data) 
        if (a_set & b_set): 
            return "Je vais t'aider avec plaisir ! Quel est ton problème ?" 

    def getExercice(self, data):
        exercices = Exercise.objects.all()
        serializer = ExerciseSerializer(exercices, many=True)
        return serializer

    def trainMyBot(self, chatterbot):
        trainerOwn = ListTrainer(chatterbot)

        #trainerOwn.train("./files/")
        #chatterbot.storage.drop()

        #Getting Help
        trainerOwn.train([
            "J'ai besoin d'aide s'il te plait !",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

        trainerOwn.train([
            "Aide-moi stp !",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

        trainerOwn.train([
            "Je peux avoir de l'aide ?",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

        trainerOwn.train([
            "tu saurais m'aider ?",
            "Bien sûr je vais t'aider avec plaisir ! Quel est ton problème ?",
        ])

         #Getting Help
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
        ])