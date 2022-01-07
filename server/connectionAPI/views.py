from os import stat
from django import db
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import psycopg2


from .serializers import DatabaseSerializer
# Create your views here.

class ConnectionViewSet(viewsets.ViewSet):

    @swagger_auto_schema(request_body=DatabaseSerializer, responses={200: DatabaseSerializer})
    @action(detail=False, methods=["post"], url_path="create")
    def connect_db(self, request, *args, **kwargs):
        db_serialized = DatabaseSerializer(data=request.data)
        if db_serialized.is_valid():
            try:
                conn = psycopg2.connect(dbname=db_serialized.validated_data["name"],
                                        host=db_serialized.validated_data["host"],
                                        port=db_serialized.validated_data["port"],
                                        user=db_serialized.validated_data["username"],
                                        password=db_serialized.validated_data["password"])
            except psycopg2.Error as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                cur = conn.cursor()
                cur.execute("SELECT * FROM information_schema.columns WHERE table_name = 'mock_data';")
                tables = cur.fetchall()
                print(tables)
                cur.close()
                conn.close()
            except psycopg2.Error as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            # for i in range(len(tables)):
            #     tables
            conn.close()
            db_serialized.save()
            return Response(data=db_serialized.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
