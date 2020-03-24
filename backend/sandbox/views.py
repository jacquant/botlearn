import html

import epicbox
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from exercises.models.exercise import Exercise
from .serializers import CodeSerializer, CodeSerializerLint, CodeSerializerExercise


def docker_run(profile, command, files, limits):
    result = epicbox.run(profile, command, files=files, limits=limits)
    result["stdout"] = result["stdout"].decode("utf-8")
    result["stderr"] = result["stderr"].decode("utf-8")
    return result


def render_main(code_input, filename):
    return html.unescape(
        render_to_string(
            "Python/main.py", {"code_input": code_input, "filename": filename}
        )
    )


class CodeExecute(APIView):
    @swagger_auto_schema(request_body=CodeSerializerExercise)
    def post(self, request, format=None):
        serializer = CodeSerializerExercise(data=request.data)
        if serializer.is_valid():
            main_code = render_main(
                serializer.validated_data["code_input"],
                serializer.validated_data["exercise_filename"],
            )
            exercise = get_object_or_404(
                Exercise, id=serializer.validated_data["exercise_id"]
            )
            profiles = [
                epicbox.Profile(
                    exercise.dockerImage.profile_name, exercise.dockerImage.image_name
                ),
            ]
            epicbox.configure(profiles=profiles)
            files = [
                {
                    "name": serializer.validated_data["exercise_filename"],
                    "content": main_code.encode(),
                }
            ]
            limits = {"cputime": 25, "memory": 64}
            result = docker_run(
                exercise.dockerImage.profile_name,
                "python {}".format(serializer.validated_data["exercise_filename"]),
                files=files,
                limits=limits,
            )
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeLint(APIView):
    @swagger_auto_schema(request_body=CodeSerializerLint)
    def post(self, request, format=None):
        serializer = CodeSerializerLint(data=request.data)
        if serializer.is_valid():
            files = [
                {
                    "name": serializer.validated_data["filename"],
                    "content": serializer.validated_data["code_input"].encode(),
                }
            ]
            limits = {"cputime": 5, "memory": 64}
            if serializer.validated_data["translate"]:
                args = "--translate "
            else:
                args = ""
            result = docker_run(
                "linter",
                "python linter.py {translate}{filename}".format(
                    translate=args, filename=serializer.validated_data["filename"]
                ),
                files=files,
                limits=limits,
            )
            if result["exit_code"]:
                result["lint_results"] = []
            else:
                result["lint_results"] = result["stdout"].splitlines()[:-1]
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
                "formatter", "black main.py && cat main.py", files=files, limits=limits
            )
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
