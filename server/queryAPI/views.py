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

            if "filter" in serialized.validated_data:
                filter_operations = serialized.validated_data["filter"][
                    "filter_operation"
                ]
                query_string += " WHERE "

                for filter in filter_operations:

                    field = Field.objects.get(id=filter["field"]["field_id"].id)
                    field_name = field.name

                    if filter["operation"] in [
                        "ends-with",
                        "contains",
                        "does-not-contain",
                        "starts-with",
                        "is-empty",
                        "is-not-empty",
                        "greater-than",
                        ">",
                        "<",
                        ">=",
                        "<=",
                        "between",
                        "=",
                        "!=",
                    ]:

                        if filter["operation"] in [
                            "ends-with",
                            "contains",
                            "does-not-contain",
                            "starts-with",
                            ">",
                            "<",
                            ">=",
                            "<=",
                        ]:
                            if filter["is_numeric"]:
                                op = int(filter["op_variable"][0])
                            else:
                                op = filter["op_variable"][0]

                        elif filter["operation"] in ["=", "!=", "between"]:

                            if filter["is_numeric"]:
                                op = tuple(float(i) for i in filter["op_variable"])
                                if len(op) == 1:
                                    op = f"({op[0]})"
                            else:
                                op = tuple(i for i in filter["op_variable"])
                                if len(op) == 1:
                                    op = f"('{op[0]}')"

                        elif filter["operation"] in ["is-empty", "is-not-empty"]:
                            op = []

                        if (
                            "type" in serialized.validated_data["filter"]
                            and len(filter["operation"]) > 1
                        ):

                            if filter["field"]["source_field"] == None:

                                if field.fk_table != source_table:

                                    return Response(
                                        data={
                                            "Message": f"field of id {field.id} does not belong to the table of id {source_table.id}"
                                        },
                                        status=status.HTTP_400_BAD_REQUEST,
                                    )
                                else:

                                    if (
                                        query_string.split(" ")[-2] == "WHERE"
                                        and query_string.split(" ")[-1]
                                        != serialized.validated_data["filter"]["type"]
                                    ):

                                        if filter["operation"] == "is-empty":
                                            query_string += f"{field_name} IS NULL {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == ">":
                                            query_string += f"{field_name} > {op} {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "<":
                                            query_string += f"{field_name} < {op} {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "<=":
                                            query_string += f"{field_name} <= {op} {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == ">=":
                                            query_string += f"{field_name} >= {op} {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "between":
                                            query_string += f"{field_name} BETWEEN {op[0]} AND {op[1]} {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "is-not-empty":
                                            query_string += f"{field_name} IS NOT NULL {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "=":
                                            query_string += f"{field_name} IN {op} {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "!=":
                                            query_string += f"{field_name} NOT IN {op} {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "ends-with":
                                            query_string += f"{field_name} LIKE '%{op}' {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "contains":
                                            query_string += f"{field_name} LIKE '%{op}%' {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "does-not-contain":
                                            query_string += f"{field_name} NOT LIKE '%{op}%' {serialized.validated_data['filter']['type']}"

                                        elif filter["operation"] == "starts-with":
                                            query_string += f"{field_name} LIKE '{op}%' {serialized.validated_data['filter']['type']}"

                                    else:
                                        if (
                                            query_string.split(" ")[-1]
                                            == serialized.validated_data["filter"][
                                                "type"
                                            ]
                                        ):
                                            query_string = query_string.rsplit(" ", 1)[
                                                0
                                            ]

                                        if filter["operation"] == "is-empty":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} IS NULL"

                                        elif filter["operation"] == ">":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} > {op}"

                                        elif filter["operation"] == "<":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} < {op}"

                                        elif filter["operation"] == "<=":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} <= {op}"

                                        elif filter["operation"] == "=<":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} =< {op}"

                                        elif filter["operation"] == "between":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} BETWEEN {op[0]} AND {op[1]}"

                                        elif filter["operation"] == "is-not-empty":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} IS NOT NULL"

                                        elif filter["operation"] == "=":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} IN {op}"

                                        elif filter["operation"] == "!=":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} NOT IN {op}"

                                        elif filter["operation"] == "ends-with":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} LIKE '%{op}'"

                                        elif filter["operation"] == "contains":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} LIKE '%{op}%'"

                                        elif filter["operation"] == "does-not-contain":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} NOT LIKE '%{op}%'"

                                        elif filter["operation"] == "starts-with":
                                            query_string += f" {serialized.validated_data['filter']['type']} {field_name} LIKE '{op}%'"

                        else:
                            if filter["operation"] == "is-empty":
                                query_string += f"{field_name} IS NULL"

                            elif filter["operation"] == ">":
                                query_string += f"{field_name} > {op}"

                            elif filter["operation"] == "<":
                                query_string += f"{field_name} < {op}"

                            elif filter["operation"] == "<=":
                                query_string += f"{field_name} <= {op}"

                            elif filter["operation"] == ">=":
                                query_string += f"{field_name} >= {op}"

                            elif filter["operation"] == "between":
                                query_string += (
                                    f"{field_name} BETWEEN {op[0]} AND {op[1]}"
                                )

                            elif filter["operation"] == "is-not-empty":
                                query_string += f"{field_name} IS NOT NULL"

                            elif filter["operation"] == "=":
                                query_string += f"{field_name} IN {op}"

                            elif filter["operation"] == "!=":
                                query_string += f"{field_name} NOT IN {op}"

                            elif filter["operation"] == "ends-with":
                                query_string += f"{field_name} LIKE '%{op}'"

                            elif filter["operation"] == "contains":
                                query_string += f"{field_name} LIKE '%{op}%'"

                            elif filter["operation"] == "does-not-contain":
                                query_string += f"{field_name} NOT LIKE '%{op}%'"

                            elif filter["operation"] == "starts-with":
                                query_string += f"{field_name} LIKE '{op}%'"

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
                        type = order["type"]
                        query_string += f"{table_name}.{field_name} {type},"

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
