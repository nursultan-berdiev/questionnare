from django.urls import path
from .views import *

urlpatterns = [
    path('quiz/create/', QuizCreateView.as_view()),
    path('quiz/detail/<int:pk>/', QuizDetailView.as_view()),
    path('quiz/all/', ActiveQuizListView.as_view()),

    path('question/create/', QuestionCreateView.as_view()),
    path('question/detail/<int:pk>', QuestionDetailView.as_view()),

    path('answer/create/', AnswerCreateView.as_view()),
    path('answer/detail/<int:pk>', AnswerDetailView.as_view()),

    path('result/create/<int:user_id>/<int:question_id>/', result_create_view),
    path('result/<int:user_id>/all/', ResultsListView.as_view()),

]