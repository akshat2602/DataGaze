from os import name, stat
from django import db
from django.db.models.fields.json import DataContains
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import psycopg2

from connectionAPI.models import Database, Table, Field

from .serializers import QuerySerializer

# Create your views here.


class FilterViewSet(viewsets.ViewSet):

    @swagger_auto_schema(request_body=QuerySerializer, responses={200: QuerySerializer})
    @action(detail=False, methods=["post"], url_path="filter")
    def filter_query(self, request):

        serialized = QuerySerializer(data=request.data)

        if serialized.is_valid():

            try:
                db = Database.objects.get(id=1)
                conn = psycopg2.connect(dbname=db.name,
                                        host=db.host,
                                        port=db.port,
                                        user=db.username,
                                        password=db.password)
            except psycopg2.Error as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                cur = conn.cursor()
            
            except psycopg2.Error as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)


            source_table = Table.objects.get(id=serialized.validated_data['source_table'].id)

            filter_operations = serialized.validated_data['filter']['filter_operation']

            for filter in filter_operations:

                field = Field.objects.get(id=filter['field']['field_id'].id)
                field_name = field.name
                table_name = source_table.name

                if filter['field']['source_field'] == None and field.fk_table == source_table:

                    if filter['operation'] == "ends-with":
                        
                        if field.data_type != "character varying":
                            op = float(filter['op_variable'][0])
                        
                        else:
                            op = filter['op_variable'][0]

                        if 'response_data' not in locals():
                            
                            cur.execute(f"SELECT * FROM {table_name} WHERE {field_name} LIKE '%{op}'")
                            
                            response_data = cur.fetchall()
                        
                        else:

                            cur.execute(f"SELECT * FROM {response_data} WHERE {field_name} LIKE '%{op}'")

                            response_data = cur.fetchall()

            return Response(data={"Message": response_data}, status=status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)