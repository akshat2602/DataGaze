from rest_framework.response import Response
from rest_framework import status

def filter_query(
    serialized, query_string, table_name, source_table, Field
):
    if "filter" in serialized.validated_data:
        filter_operations = serialized.validated_data["filter"]["filter_operation"]
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

                    print(f"=============={op}===============")

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
                    "type_" in serialized.validated_data["filter"]
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
                                != serialized.validated_data["filter"]["type_"]
                            ):
                                print(
                                    f'================={filter["operation"]}================'
                                )
                                if filter["operation"] == "is-empty":
                                    query_string += f"{table_name}.{field_name} IS NULL {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == ">":
                                    query_string += f"{table_name}.{field_name} > {op} {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "<":
                                    query_string += f"{table_name}.{field_name} < {op} {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "<=":
                                    query_string += f"{table_name}.{field_name} <= {op} {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == ">=":

                                    query_string += f"{table_name}.{field_name} >= {op} {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "between":
                                    query_string += f"{table_name}.{field_name} BETWEEN {op[0]} AND {op[1]} {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "is-not-empty":
                                    query_string += f"{table_name}.{field_name} IS NOT NULL {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "=":
                                    query_string += f"{table_name}.{field_name} IN {op} {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "!=":
                                    query_string += f"{table_name}.{field_name} NOT IN {op} {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "ends-with":
                                    query_string += f"{table_name}.{field_name} LIKE '%{op}' {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "contains":
                                    query_string += f"{table_name}.{field_name} LIKE '%{op}%' {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "does-not-contain":
                                    query_string += f"{table_name}.{field_name} NOT LIKE '%{op}%' {serialized.validated_data['filter']['type_']}"

                                elif filter["operation"] == "starts-with":
                                    query_string += f"{table_name}.{field_name} LIKE '{op}%' {serialized.validated_data['filter']['type_']}"

                            else:

                                if (
                                    query_string.split(" ")[-1]
                                    == serialized.validated_data["filter"]["type_"]
                                ):
                                    print(
                                        f'================={filter["operation"]}================'
                                    )
                                    query_string = query_string.rsplit(" ", 1)[0]

                                if filter["operation"] == "is-empty":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} IS NULL"

                                elif filter["operation"] == ">":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} > {op}"

                                elif filter["operation"] == "<":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} < {op}"

                                elif filter["operation"] == "<=":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} <= {op}"

                                elif filter["operation"] == ">=":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} >= {op}"

                                elif filter["operation"] == "between":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} BETWEEN {op[0]} AND {op[1]}"

                                elif filter["operation"] == "is-not-empty":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} IS NOT NULL"

                                elif filter["operation"] == "=":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} IN {op}"

                                elif filter["operation"] == "!=":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} NOT IN {op}"

                                elif filter["operation"] == "ends-with":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} LIKE '%{op}'"

                                elif filter["operation"] == "contains":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} LIKE '%{op}%'"

                                elif filter["operation"] == "does-not-contain":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} NOT LIKE '%{op}%'"

                                elif filter["operation"] == "starts-with":
                                    query_string += f" {serialized.validated_data['filter']['type_']} {table_name}.{field_name} LIKE '{op}%'"

                else:
                    if filter["operation"] == "is-empty":
                        query_string += f"{table_name}.{field_name} IS NULL"

                    elif filter["operation"] == ">":
                        query_string += f"{table_name}.{field_name} > {op}"

                    elif filter["operation"] == "<":
                        query_string += f"{table_name}.{field_name} < {op}"

                    elif filter["operation"] == "<=":
                        query_string += f"{table_name}.{field_name} <= {op}"

                    elif filter["operation"] == ">=":
                        query_string += f"{table_name}.{field_name} >= {op}"

                    elif filter["operation"] == "between":
                        query_string += (
                            f"{table_name}.{field_name} BETWEEN {op[0]} AND {op[1]}"
                        )

                    elif filter["operation"] == "is-not-empty":
                        query_string += f"{table_name}.{field_name} IS NOT NULL"

                    elif filter["operation"] == "=":
                        query_string += f"{table_name}.{field_name} IN {op}"

                    elif filter["operation"] == "!=":
                        query_string += f"{table_name}.{field_name} NOT IN {op}"

                    elif filter["operation"] == "ends-with":
                        query_string += f"{table_name}.{field_name} LIKE '%{op}'"

                    elif filter["operation"] == "contains":
                        query_string += f"{table_name}.{field_name} LIKE '%{op}%'"

                    elif filter["operation"] == "does-not-contain":
                        query_string += f"{table_name}.{field_name} NOT LIKE '%{op}%'"

                    elif filter["operation"] == "starts-with":
                        query_string += f"{table_name}.{field_name} LIKE '{op}%'"

    return query_string
