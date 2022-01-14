from email.policy import default
from django.core.exceptions import ValidationError
from rest_framework import serializers

from connectionAPI.models import Field, Table
from .validate import validate_field


class FieldSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=20)
    field_id = serializers.PrimaryKeyRelatedField(
        queryset=Field.objects.all(), many=False
    )
    source_field = serializers.PrimaryKeyRelatedField(
        queryset=Field.objects.all(), many=False, allow_null=True
    )


OPERATION_CHOICES = [
    "starts-with",
    "contains",
    "does-not-contain",
    "is-empty",
    "not-empty",
    "ends-with",
    "!=",
    "=",
    ">=",
    "<=",
    ">",
    "<",
    "between",
]


class FilterFunctionSerializer(serializers.Serializer):
    operation = serializers.CharField(max_length=20)
    field = FieldSerializer(many=False)
    is_numeric = serializers.BooleanField(default=False)
    op_variable = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False
    )

    def validate_operation(self, operation):

        global OPERATION_CHOICES

        validate_field(operation, OPERATION_CHOICES)

        return operation

    def validate(self, data):

        global OPERATION_CHOICES

        if "op_variable" in data:
            if data["operation"] == "is-empty" or data["operation"] == "is-not-empty":
                if len(data["op_variable"]) != 0:
                    raise ValidationError("op_variable not required")

            if data["is_numeric"]:
                try:
                    check = [float(item) for item in data["op_variable"]]
                except:
                    raise ValidationError("op_variable must contain only numeric")

        if data["operation"] in [">", "<", ">=", "<=", "between"]:

            if not data["is_numeric"]:
                raise ValidationError(
                    "is_numeric must be true for this filter operation"
                )

        if (
            data["operation"] == "starts-with"
            or data["operation"] == "contains"
            or data["operation"] == "does-not-contain"
            or data["operation"] == "ends-with"
            or data["operation"] == ">"
            or data["operation"] == "<"
            or data["operation"] == ">="
            or data["operation"] == "<="
        ):

            if len(data["op_variable"]) != 1:
                raise ValidationError("only 1 op_variable needed for this operation")

        if data["operation"] == "between":

            if len(data["op_variable"]) != 2:
                raise ValidationError("exactly 2 op_variable needed for this operation")

        elif data["operation"] == "=" or data["operation"] == "!=":

            if len(data["op_variable"]) < 1:
                raise ValidationError("atleast 1 op_variable needed for this operation")

        # elif(data['operation'] == 'is-empty' or data['operation'] == 'is-not-empty'):

        #     if len(data['op_variable']) !=0:
        #         raise ValidationError("op_variable must be empty")

        return super().validate(data)


class FilterSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=20, required=False)
    filter_operation = FilterFunctionSerializer(many=True)

    def validate_type(self, type):

        TYPE_CHOICES = ["and", "or"]
        validate_field(type, TYPE_CHOICES)

        return type

    def validate(self, data):

        if len(data["filter_operation"]) > 1 and "type" not in data:
            raise ValidationError("type must be specified for more than one filters")

        return super().validate(data)


class OrderSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10, required=True)
    field = FieldSerializer(many=False)

    def validate_type(self, type):

        TYPE_CHOICES = ["asc", "desc"]
        validate_field(type, TYPE_CHOICES)

        return type


class JoinSerializer(serializers.Serializer):
    strategy = serializers.CharField(max_length=25, default="inner_join")
    lhs = FieldSerializer(many=False)
    rhs = FieldSerializer(many=False)
    source_table = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(), many=False
    )


class QuerySerializer(serializers.Serializer):
    source_table = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(), many=False
    )
    filter = FilterSerializer(many=False, required=False)
    order = OrderSerializer(many=True, required=False)
    join = JoinSerializer(many=True, required=False)
    limit = serializers.IntegerField(required=False)

    def validate(self, data):
        join = data['join']
        source_table = data['source_table']
        for single_join in join:
            lhs = single_join['lhs']['field_id']
            rhs = single_join['rhs']['field_id']
            rhs_table = single_join['source_table']
            
            try:
                Field.objects.get(id=lhs.id, fk_table=source_table.id)
            except Field.DoesNotExist:
                raise ValidationError("Wrong field id provided for the source table")

            try: 
                Field.objects.get(id=rhs.id, fk_table=rhs_table.id)
            except Field.DoesNotExist:
                raise ValidationError("Wrong field id provided for the joining table")


        return super().validate(data)
