from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeSerializer

from codejail.safe_exec import safe_exec

import sys
from io import StringIO
import contextlib


@contextlib.contextmanager
def stdout_io(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class CodeView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        code_serializer = CodeSerializer(data=request.data)
        if code_serializer.is_valid():
            with stdout_io() as s:
                try:
                    output = safe_exec(code_serializer.validated_data["code_input"], {})
                    print(output)
                except Exception as e:
                    pass
                output = s.getvalue()
                code_serializer.save()
                return Response(output, status=status.HTTP_200_OK)
        else:
            return Response(code_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
