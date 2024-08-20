    


from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated


class Foo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, req, format=None):
        data = {
            "word": "hello",
            "bet": "world",
        }
        return JsonResponse(data, status=status.HTTP_200_OK)