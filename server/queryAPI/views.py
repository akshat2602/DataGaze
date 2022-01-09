from os import name, stat
from django import db
from django.db.models.fields.json import DataContains
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import psycopg2

from .serializers import QuerySerializer

# Create your views here.


class FilterViewSet(viewsets.ViewSet):

    @swagger_auto_schema(request_body=QuerySerializer, responses={200: QuerySerializer})
    @action(detail=False, methods=["post"], url_path="filter")
    def filter_query(self, request):

        serialized = QuerySerializer(data=request.data)

        if serialized.is_valid():
            
            return Response(data={"Message": "Valid"}, status=status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)