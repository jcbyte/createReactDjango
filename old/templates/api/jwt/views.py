from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User

# Create your views here.


class CreateUser(APIView):
    def post(self, request):
        user = User(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()

        return Response(status=status.HTTP_201_CREATED)