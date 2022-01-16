from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import psycopg2

from connectionAPI.models import Database, Table, Field

from .serializers import QuerySerializer
from .utils import filter_query

# Create your views here.


class FilterViewSet(viewsets.ViewSet):
    @swagger_auto_schema(request_body=QuerySerializer, responses={200: QuerySerializer})
    @action(detail=False, methods=["post"], url_path="filter")
    def filter_query(self, request):

        serialized = QuerySerializer(data=request.data)

        if serialized.is_valid():

            source_table = Table.objects.get(
                id=serialized.validated_data["source_table"].id
            )
            table_name = source_table.name
            query_string = f"SELECT * FROM {table_name}"

            if "join" in serialized.validated_data:
                for join in serialized.validated_data["join"]:
                    if join["strategy"] == "inner_join":
                        query_string += " INNER JOIN "
                    elif join["strategy"] == "left_outer_join":
                        query_string += " LEFT JOIN "
                    elif join["strategy"] == "right_outer_join":
                        query_string += " RIGHT JOIN "
                    elif join["strategy"] == "full_outer_join":
                        query_string += " FULL JOIN "
                    print(join)
                    rhs_table_name = Table.objects.get(id=join["source_table"].id).name
                    lhs_field_name = Field.objects.get(
                        id=join["lhs"]["field_id"].id
                    ).name
                    rhs_field_name = Field.objects.get(
                        id=join["rhs"]["field_id"].id
                    ).name

                    query_string += f"{rhs_table_name} ON {table_name}.{lhs_field_name}={rhs_table_name}.{rhs_field_name}"
            

            query_string = filter_query(serialized, query_string, table_name, source_table, Field)
            if(type("str") != type(query_string)):
                return query_string

            
            if "order" in serialized.validated_data:
                query_string += " ORDER BY "

                for order in serialized.validated_data["order"]:
                    field = Field.objects.get(id=order["field"]["field_id"].id)
                    field_name = field.name

                    if order["field"]["source_field"] != None:
                        if field.fk_table != source_table:
                            return Response(
                                data={
                                    "Message": f"Field of id {field.id} does not belong to the table of id {source_table.id}"
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    else:
                        type_ = order["type_"]
                        query_string += f"{table_name}.{field_name} {type_},"

            if "order" in serialized.validated_data:
                query_string = query_string[:-1]

            if "limit" in serialized.validated_data:
                query_string += " LIMIT " + str(serialized.validated_data["limit"])
            query_string += ";"
            print(query_string)

            try:
                db = Database.objects.get(id=1)
                conn = psycopg2.connect(
                    dbname=db.name,
                    host=db.host,
                    port=db.port,
                    user=db.username,
                    password=db.password,
                )
            except psycopg2.Error as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                cur = conn.cursor()

            except psycopg2.Error as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                cur.execute(query_string)
                table_data = cur.fetchall()
            except:
                return Response(
                    data={"Error": "Couldn't fetch data!"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                data={"Query": query_string, "Response": table_data},
                status=status.HTTP_200_OK,
            )

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)
