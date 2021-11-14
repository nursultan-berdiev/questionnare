from rest_framework import serializers
from .models import Quiz, Question, Answer, Result


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['chosen_answer', 'written_answer']


class ResultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['user_id', 'question', 'chosen_answer', 'written_answer']
