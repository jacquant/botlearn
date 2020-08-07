import html
import re

from celery import shared_task
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

import epicbox
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.user import User
from exercises.models import (
    Error,
    ErrorCount,
    Exercise,
    Submission,
)
from sandbox.serializers import (
    CodeSerializer,
    CodeSerializerExercise,
    CodeSerializerLint,
)


def count_errors(list_results):
    """Build a set of code and count of errors from list of error's message.

    :param list_results: list of string errors
    :type list_results: list
    :return: a set of tuples (error_code, counter)
    :rtype: set
    """
    pattern = re.compile(r"(?<=: )[A-Z]{1,3}[0-9]{1,3}(?= )")
    errors = {}
    for error in list_results:
        match = pattern.search(error)
        if match:
            if match[0] in errors:
                errors[match[0]] += 1  # noqa: WPS529
            else:
                errors[match[0]] = 1  # noqa: WPS529
    return errors.items()


@shared_task
def create_submission(author_mail, exercise_id, code, output, final):
    """Update the database with the call of the API.

    :param author_mail: the mail of the user that made the request
    :type author_mail: str
    :param exercise_id: the id of the exercise
    :type exercise_id: int
    :param code: the code sent in the view
    :type code: str
    :param output: the output from the sandbox
    :type output: dict
    :param final: if the submission is final
    :type final: bool
    """
    author = User.objects.get(mail=author_mail)
    exercise = Exercise.objects.get(id=exercise_id)
    submission = Submission.objects.create(
        author=author,
        exercise=exercise,
        code_input=code,
        code_output=output,
        not_executed=bool(output["exit_code"]),
        final=final,
    )
    for code_error, count_error in count_errors(output["lint_results"]):
        error, _created = ErrorCount.objects.get_or_create(
            error=Error.objects.get_or_create(code=code_error)[0],
            counter=count_error,
        )
        submission.errors.add(error)


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


def render_main(code_input):
    """Render the template with the code given.

    :param code_input: the field used to render the code
    :type code_input: str
    :return: a string rendered with the field and with html balise removed
    :rtype: str
    """
    return html.unescape(
        render_to_string("Python/main.py", {"code_input": code_input}),
    )


class CodeExecute(APIView):
    """Execute code API view."""

    @swagger_auto_schema(request_body=CodeSerializerExercise)
    def post(self, request):
        """Post method to execute code."""
        serializer = CodeSerializerExercise(data=request.data)
        if serializer.is_valid():
            main_code = render_main(
                serializer.validated_data["code_input"],
            )
            exercise = get_object_or_404(
                Exercise, id=serializer.validated_data["exercise_id"],
            )
            epicbox.configure(
                profiles=[
                    epicbox.Profile(
                        exercise.docker_image.profile_name,
                        exercise.docker_image.image_name,
                    ),
                ]
            )
            result_run1 = docker_run(
                exercise.docker_image.profile_name,
                "python {0}".format(serializer.validated_data["filename"]),
                files=[
                    {
                        "name": serializer.validated_data["filename"],
                        "content": main_code.encode(),
                    },
                ],
                limits={"cputime": 50, "memory": 128},
            )
            errors_set = set()
            for template in exercise.errors_template.all():
                for error in template.errors.all().distinct().values_list("code", flat=True):
                    errors_set.add(error)
            if len(errors_set) > 0:
                errors_string = " ".join(errors_set)
            else:
                errors_string = None
            result_run2 = lint(serializer, errors_string)
            result_run1["lint_results"] = result_run2["lint_results"]
            create_submission.delay(
                self.request.user.mail,
                serializer.validated_data["exercise_id"],
                serializer.validated_data["code_input"],
                result_run1,
                serializer.validated_data["final"],
            )
            return Response(result_run1, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeLint(APIView):
    """Lint code view."""

    @swagger_auto_schema(request_body=CodeSerializerLint)
    def post(self, request):
        """Post method to lint code."""
        serializer = CodeSerializerLint(data=request.data)
        if serializer.is_valid():
            result_run = lint(serializer)
            return Response(result_run, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def lint(serializer, errors_str=None):
    """Lint function."""
    files = [
        {
            "name": serializer.validated_data["filename"],
            "content": serializer.validated_data["code_input"].encode(),
        },
    ]
    limits = {"cputime": 50, "memory": 128}
    try:
        if serializer.validated_data["translate"]:
            args = "--translate "
        else:
            args = ""
    except KeyError:
        args = ""
    if errors_str is None:
        command = "python linter.py {translate}{filename}".format(
            translate=args, filename=serializer.validated_data["filename"],
        )
    else:
        command = "python linter.py {translate}{filename} --errors {errors}".format(
            translate=args, filename=serializer.validated_data["filename"], errors=errors_str,
        )
    result_run = docker_run(
        "linter",
        command,
        files=files,
        limits=limits,
    )
    if result_run["exit_code"]:
        result_run["lint_results"] = []
    else:
        result_run["lint_results"] = result_run["stdout"].splitlines()[:-1]
    return result_run


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
