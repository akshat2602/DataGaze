from django.db.models import fields
from rest_framework import serializers

from .models import *


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = "__all__"
