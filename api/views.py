from rest_framework import viewsets
from .models import TestData
from .serializers import TestDataSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class TestDataViewSet(viewsets.ModelViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer

class HelloWorld(APIView):
    def get(self, request, format=None):
        return Response({"message": "Hello World!!"},
            status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        return Response({"success": True, "predictedWord": "あ"},
            status=status.HTTP_201_CREATED)