import html

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

import epicbox
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from exercises.models.exercise import Exercise
from sandbox.serializers import (
    CodeSerializer,
    CodeSerializerExercise,
    CodeSerializerLint,
)


def docker_run(profile, command, files, limits):
    """Function used to run a specific command in a docker image.

    :param profile: the profile linked to the docker image
    :type profile: str
    :param command: the shell command executed in the docker
    :type command: str
    :param files: The files to copy in the sandbox
    :type files: list
    :param limits: limits to use that will rules the sandbox
    :type limits: dict
    :return: a dictionary with all the contents produce by the sandbox
    :rtype: dict
    """
    run_result = epicbox.run(profile, command, files=files, limits=limits)
    # Decode the stdout and the stderr
    run_result["stdout"] = run_result["stdout"].decode("utf-8")
    run_result["stderr"] = run_result["stderr"].decode("utf-8")
    return run_result


def render_main(code_input, filename):
    """Render the template withe the code given.

    :param code_input: the field used to render the code
    :type code_input: str
    :param filename: the name of the file that will be executed
    :type filename: str
    :return: a string rendered with the field and with html balise removed
    :rtype: str
    """
    return html.unescape(
        render_to_string(
            "Python/main.py", {"code_input": code_input, "filename": filename}
        ),
    )


class CodeExecute(APIView):
    """Execute code API view."""

    @swagger_auto_schema(request_body=CodeSerializerExercise)
    def post(self, request):
        """Post method to execute code.

        :param request: [description]
        :type request: [type]
        :return: [description]
        :rtype: [type]
        """
        serializer = CodeSerializerExercise(data=request.data)
        if serializer.is_valid():
            main_code = render_main(
                serializer.validated_data["code_input"],
                serializer.validated_data["exercise_filename"],
            )
            exercise = get_object_or_404(
                Exercise, id=serializer.validated_data["exercise_id"],
            )
            profiles = [
                epicbox.Profile(
                    exercise.docker_image.profile_name,
                    exercise.docker_image.image_name,
                ),
            ]
            epicbox.configure(profiles=profiles)
            result_run = docker_run(
                exercise.docker_image.profile_name,
                "python {0}".format(
                    serializer.validated_data["exercise_filename"]
                ),
                files=[
                    {
                        "name": serializer.validated_data["exercise_filename"],
                        "content": main_code.encode(),
                    },
                ],
                limits={"cputime": 25, "memory": 64},
            )
            return Response(result_run, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeLint(APIView):
    """Lint code view."""

    @swagger_auto_schema(request_body=CodeSerializerLint)
    def post(self, request):
        """Post method to lint code."""
        serializer = CodeSerializerLint(data=request.data)
        if serializer.is_valid():
            files = [
                {
                    "name": serializer.validated_data["filename"],
                    "content": serializer.validated_data[
                        "code_input"
                    ].encode(),
                },
            ]
            limits = {"cputime": 5, "memory": 64}
            if serializer.validated_data["translate"]:
                args = "--translate "
            else:
                args = ""
            result_run = docker_run(
                "linter",
                "python linter.py {translate}{filename}".format(
                    translate=args,
                    filename=serializer.validated_data["filename"],
                ),
                files=files,
                limits=limits,
            )
            if result_run["exit_code"]:
                result_run["lint_results"] = []
            else:
                result_run["lint_results"] = result_run["stdout"].splitlines()[
                    :-1
                ]
            return Response(result_run, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeFormat(APIView):
    """Format code API view."""

    @swagger_auto_schema(request_body=CodeSerializer)
    def post(self, request):
        """Post method to format code with black utility."""
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            files = [
                {
                    "name": "main.py",
                    "content": serializer.validated_data[
                        "code_input"
                    ].encode(),
                },
            ]
            limits = {"cputime": 5, "memory": 64}
            result_run = docker_run(
                "formatter",
                "black main.py && cat main.py",
                files=files,
                limits=limits,
            )
            return Response(result_run, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
