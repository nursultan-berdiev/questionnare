import datetime
from rest_framework import generics, status
from .serializers import *
from .models import Quiz, Question, Answer, Result
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .serializers import ResultSerializer


class QuizCreateView(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = (IsAdminUser,)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAdminUser,)


class ActiveQuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all().filter(end_date__gt=datetime.datetime.now())
    serializer_class = QuizSerializer


class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAdminUser,)


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (IsAdminUser,)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAdminUser,)


class ResultsListView(generics.ListAPIView):
    serializer_class = ResultListSerializer
    queryset = Result.objects.all()

    def list(self, request, user_id):
        queryset = Result.objects.filter(user_id=user_id).select_related('question', 'chosen_answer')
        serializer = ResultListSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST', 'GET'])
def result_create_view(request, user_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        answers = Answer.objects.all().filter(question=question)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        results = Result(question=question, user_id=user_id)
        serializer = ResultSerializer(results, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
