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

from datetime import datetime, time


class AnswerViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated]
    #Defined and train the bot
    chatterbot = ChatBot(**settings.CHATTERBOT,
                        read_only=True,
                        
                        logic_adapters=[{
                            'maximum_similarity_threshold': 0.85,
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
        print(type(response))
        #response += self.getExercice()

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

    def needHelp(self, data):
        a_set = set(["aide","aider","besoin d'aide","help"]) 
        b_set = set(data) 
        if (a_set & b_set): 
            return "Je vais t'aider avec plaisir ! Quel est ton problème ?" 

    def getExercice(self, data=None):
        exercices = Exercise.objects.all()
        serializer = ExerciseSerializer(exercices, many=True)

        #Get Current Time
        now = datetime.now()

        exercices_string = ""
        #print(serializer.data)

        for exercice in serializer.data:
            for info in exercice.items():
                if(info[0] ==  "name"):
                    name = info[1]
                if(info[0] ==  "due_date"):
                    time = datetime.strptime(info[1],'%Y-%m-%dT%H:%M:%S%fZ')
                if (info[0] == "project_files"):
                    path = info[1]
                    if (now < time):
                        exercices_string +='- <a href="http://localhost:8080' + str(path) +'">' + name + " (à rendre pour le "+ str(time) + ")</a>" + "<br>"

        #print(exercices_string)
        return exercices_string

    def trainMyBot(self, chatterbot):
        #chatterbot.storage.drop()

        #Corpus Part
        trainerCoprus = ChatterBotCorpusTrainer(chatterbot)

        trainerCoprus.train('chatterbot.corpus.french')
        


        #trainerOwn.train("./files/")


        #Own training
        trainerOwn = ListTrainer(chatterbot)

        #Getting Help
        trainerOwn.train([
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

        """#Problem With loop
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

        #Getting Exercices
        trainerOwn.train([
            "Je peux avoir la liste des exercice",
            "Oui ! La voici: <br>",
        ])

        trainerOwn.train([
            "Quels sont les exercices à faire ?",
            "Voici les exercices à faire:" + self.getExercice(),
        ])

        trainerOwn.train([
            "On doit faire quoi comme devoir ?",
            "Voici les exercices à faire:" + self.getExercice(),
        ])

        trainerOwn.train([
            "Donne moi la liste des devoirs ?",
            "Voici les exercices à faire:" + self.getExercice(),
        ])
