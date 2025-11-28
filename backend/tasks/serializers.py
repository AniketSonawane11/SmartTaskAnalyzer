from rest_framework import serializers
from .models import Task


# 1) For saving task in database
class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# 2) For analyze and suggest input (NOT saved to DB)
class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    due_date = serializers.DateField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField()
    importance = serializers.IntegerField()
    dependencies = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )


# 3) For Analyze API request body
class AnalyzeRequestSerializer(serializers.Serializer):
    tasks = TaskInputSerializer(many=True)
    strategy = serializers.CharField(required=False)
