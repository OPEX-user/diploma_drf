from django.urls import path

from .views import (
    SurveyView,
    SurveyDetailView,
    QuestionView,
    QuestionDetailsView,
    AnswerOptionView,
    AnswerOptionDetailsView,
    UserResponseView,
    UserResponseDetailsView,
    UserView,
    UserDetailsView,
    RegisterView,
    LoginView,
    UserRegisterView,
    LogoutView,
    change_password,
    RequestPasswordReset,
    ResetPassword,
)

urlpatterns = [
    path('survey/', SurveyView.as_view()),
    path('survey/<int:pk>/', SurveyDetailView.as_view()),
    path('question/', QuestionView.as_view()),
    path('question/<int:pk>/', QuestionDetailsView.as_view()),
    path('answer/', AnswerOptionView.as_view()),
    path('answer/<int:pk>/', AnswerOptionDetailsView.as_view()),
    path('responses/', UserResponseView.as_view()),
    path('responses/<int:pk>/', UserResponseDetailsView.as_view()),
    path('user/', UserView.as_view()),
    path('user/<int:pk>/', UserDetailsView.as_view()),

    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserRegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', change_password, name='change_password'),
    path('request_password/', RequestPasswordReset.as_view()),
    path('reset_password/', ResetPassword.as_view())
]
