import random

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView


def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class Foo(APIView):
    def get(self, req, format=None):
        data = {
            "text": f"Hello React",
            "color": get_random_color(),
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
