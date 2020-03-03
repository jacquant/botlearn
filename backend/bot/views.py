from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from exercises.models.exercise import Exercise
from exercises.serializers.exercise import ExerciseSerializer

#from chatterbot import ChatBot

class AnswerViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated]
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

        return Response(content)

    def needHelp(self, data):
        a_set = set(["aide","aider","besoin d'aide","help"]) 
        b_set = set(data) 
        if (a_set & b_set): 
            return "Je vais t'aider avec plaisir ! Quel est ton problème ?" 

    def getExercice(self, data):
        exercices = Exercise.objects.all()
        serializer = ExerciseSerializer(exercices, many=True)
        return serializer