from rest_framework import serializers
from .models import TestResult, Question
from accounts.serializers import UserSerializer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class TestResultDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TestResult
        fields = '__all__'


class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    rank = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test_name', 'test_type', 'obtained_marks', 'total_marks',
                  'percentage', 'correct', 'wrong', 'skipped', 'total_questions',
                  'time_taken_seconds', 'created_at', 'rank']


class HistoryStatsSerializer(serializers.Serializer):
    total_tests = serializers.IntegerField()
    total_marks_obtained = serializers.FloatField()
    total_marks_possible = serializers.FloatField()
    average_percentage = serializers.FloatField()
    best_score = serializers.FloatField()
    last_test_date = serializers.DateTimeField()
