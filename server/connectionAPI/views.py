from os import name, stat
from django import db
from django.db.models.fields.json import DataContains
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import psycopg2

from connectionAPI.models import Database, Field, Table


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
                cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
                
                tables = cur.fetchall()
                table_response = []                
                
                print(table_response)
                
            except psycopg2.Error as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            # for i in range(len(tables)):
            #     tables

            db_serialized.save()

            try:
                for table in tables:
                    ob = Table(name = str(table[0]), fk_database = Database.objects.get(pk =db_serialized.data['id']))
                    ob.save()
                    
                    cur.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{str(table[0]).lower()}';")
                    fields = cur.fetchall()
                    final_fields = [[field[0], field[1]] for field in fields]
                    print(final_fields)
                    Field.objects.bulk_create([
                        Field(name = str(field[0]), data_type=str(field[1]), fk_table=ob) for field in final_fields
                    ])
                    
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

                # for field in final_fields:
                #     field_ob = Field(name = str(field[0]), data_type=str(field[1]), fk_table=ob)
                #     field_ob.save()

                # for field in fields:
                #     field_ob = Field(name = str[field[0]])
                # print(fields)

            cur.close()
            conn.close()

            return Response(data=db_serialized.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
