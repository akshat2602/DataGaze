from django.core.exceptions import ValidationError
from rest_framework import serializers
from connectionAPI.models import Database, Field, Table

class FieldSerializer(serializers.Serializer):
    field = serializers.CharField(max_length = 20)
    field_id = serializers.PrimaryKeyRelatedField(queryset = Field.objects.all(), many=False)
    source_field = serializers.PrimaryKeyRelatedField(queryset = Field.objects.all(), many=False, allow_null=True)

class FilterFunctionSerializer(serializers.Serializer):
    operation = serializers.CharField(max_length = 20)
    field = FieldSerializer(many=False)
    op_variable = serializers.ListField(
        child = serializers.CharField(max_length = 100)
    )

    def validate_operation(self, operation):

        OPERATION_CHOICES = [
                    "starts-with",
                    "contains",
                    "=",
                    "!=",
                    "does-not-contain",
                    "is-empty",
                    "not-empty",
                    "ends-with"
                ]
        
        if operation not in OPERATION_CHOICES:
            raise ValidationError("invalid filter operation")
        
        return operation

class FilterSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=20, required=False)
    filter_operation = FilterFunctionSerializer(many=True)

    
    def validate_type(self, type):
        
        TYPE_CHOICES = [
            "and"
        ]
        
        if type not in TYPE_CHOICES:
            raise ValidationError("invalid type of filter")
        
        return type


class QuerySerializer(serializers.Serializer):
    source_table = serializers.PrimaryKeyRelatedField(queryset = Table.objects.all(), many=False)
    filter = FilterSerializer(many=False)
