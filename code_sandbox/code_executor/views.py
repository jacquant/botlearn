from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeSerializer

from codejail.safe_exec import safe_exec


class CodeView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        code_serializer = CodeSerializer(data=request.data)
        if code_serializer.is_valid():
            output = safe_exec(code_serializer.data["code_input"])
            print(output)
            code_serializer.save(output_code=output)
            return Response(output, status=status.HTTP_200_OK)
        else:
            return Response(code_serializer.errors, status=status.HTTP_400_BAD_REQUEST)