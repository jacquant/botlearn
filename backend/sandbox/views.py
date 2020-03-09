from rest_framework.views import APIView
from rest_framework.response import Response
import epicbox
import zipfile
from rest_framework import status
from exercises.models.exercise import Exercise
from .serializers import CodeSerializer, CodeSerializerExercise
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
import uuid


def docker_run(profile, command, files, limits):
    result = epicbox.run(profile, command, files=files, limits=limits)
    result["stdout"] = result["stdout"].decode("utf-8")
    result["stderr"] = result["stderr"].decode("utf-8")
    return result


class CodeExecute(APIView):
    @swagger_auto_schema(request_body=CodeSerializerExercise)
    def post(self, request, format=None):
        serializer = CodeSerializerExercise(data=request.data)
        if serializer.is_valid():
            profiles = [
                epicbox.Profile("executor", "epicbox-executer:latest"),
                epicbox.Profile("linter", "epicbox-linter:latest"),
                epicbox.Profile("formatter", "epicbox-formatter:latest"),
            ]

            epicbox.configure(profiles=profiles)
            exercise = get_object_or_404(
                Exercise, id=serializer.validated_data["exercise_id"]
            )
            files = [
                {
                    "name": "main.py",
                    "content": serializer.validated_data["code_input"].encode(),
                }
            ]
            limits = {"cputime": 25, "memory": 64}
            result = docker_run("executor", "python main.py", files=files, limits=limits,)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeLint(APIView):
    @swagger_auto_schema(request_body=CodeSerializer)
    def post(self, request, format=None):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            files = [
                {
                    "name": "main.py",
                    "content": serializer.validated_data["code_input"].encode(),
                }
            ]
            limits = {"cputime": 5, "memory": 64}
            result = docker_run("linter", "flake8 main.py", files=files, limits=limits)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeFormat(APIView):
    @swagger_auto_schema(request_body=CodeSerializer)
    def post(self, request, format=None):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            files = [
                {
                    "name": "main.py",
                    "content": serializer.validated_data["code_input"].encode(),
                }
            ]
            limits = {"cputime": 5, "memory": 64}
            result = docker_run(
                "formatter", "black --diff main.py", files=files, limits=limits
            )
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
