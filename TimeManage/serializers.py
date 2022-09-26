from dataclasses import fields
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    name = serializers.CharField()
    is_staff = serializers.BooleanField()
    date_joined = serializers.DateTimeField()
    is_active = serializers.BooleanField()

class StylesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardStyles
        fields = "__all__"

class LabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratories
        fields = "__all__"

class ReadySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyTasks
        fields = "__all__"

class RelationSerializer(serializers.ModelSerializer):
    styleID = StylesSerializer()
    labID = LabsSerializer()
    class Meta:
        model = Relations
        fields = ['styleID','labID']

class TotalSerializer(serializers.Serializer):
    count = serializers.IntegerField()