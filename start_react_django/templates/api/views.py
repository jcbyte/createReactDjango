from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

class Foo(APIView):
    def get(self, req, format=None):
        data = {
            "word": "hello",
            "bet": "world",
        }
        return JsonResponse(data, status=status.HTTP_200_OK)