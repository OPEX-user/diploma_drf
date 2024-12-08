from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

import os
import jwt
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .send_mail import send_mail
from .models import (
    Survey,
    Question,
    AnswerOption,
    UserResponse,
    User,
    PasswordReset,
)
from .serializer import (
    SurveySerializer,
    QuestionSerializer,
    OneQuestionSerializer,
    AnswerOptionSerializer,
    UserResponseSerializer,
    OneUserResponseSerializer,
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer
)


class IsGetOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return bool(request.user and request.user.is_staff)


class AdminPermission(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False


class SurveyView(APIView):
    permission_classes = (IsGetOrIsAuthenticated, AdminPermission,)

    @staticmethod
    def get(request):
        survey = Survey.objects.all()
        serializer = SurveySerializer(survey, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            survey_object = serializer.save()
            return Response(f'Опрос *{survey_object}* успешно создан')


class SurveyDetailView(APIView):
    permission_classes = (IsGetOrIsAuthenticated, AdminPermission,)

    @staticmethod
    def get(request, pk):
        survey_object = get_object_or_404(Survey.objects.all(), pk=pk)
        survey_serializer = SurveySerializer(survey_object)
        questions = Question.objects.filter(survey=pk)
        questions_serializer = OneQuestionSerializer(questions, many=True)
        answer = AnswerOption.objects.all()
        answer_serializer = AnswerOptionSerializer(answer, many=True)
        response = UserResponse.objects.all()
        response_serializer = OneUserResponseSerializer(response, many=True)
        return Response({
            'Опрос': survey_serializer.data,
            'Вопросы': questions_serializer.data,
            'Ответы': answer_serializer.data,
            'Ответы пользователя': response_serializer.data
        })

    @staticmethod
    def put(request, pk):
        survey_object = get_object_or_404(Survey.objects.all(), pk=pk)
        serializer = SurveySerializer(instance=survey_object, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            survey_object = serializer.save()
            return Response(f'Опрос *{survey_object}* успешно обновлен')

    @staticmethod
    def delete(request, pk):
        survey_object = get_object_or_404(Survey.objects.all(), pk=pk)
        survey_object.delete()
        return Response(f'Опрос *{survey_object}* был удален', status=204)


class QuestionView(APIView):
    permission_classes = (IsGetOrIsAuthenticated, AdminPermission)

    @staticmethod
    def get(request):
        questions = Question.objects.all()
        serializer = OneQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            question_object = serializer.save()
            return Response(f'Вопрос *{question_object}* успешно создан')


class QuestionDetailsView(APIView):
    permission_classes = (IsGetOrIsAuthenticated, AdminPermission,)

    @staticmethod
    def get(request, pk):
        question_object = get_object_or_404(Question.objects.all(), pk=pk)
        question_serializer = OneQuestionSerializer(question_object)
        answer = AnswerOption.objects.filter(question=pk)
        answer_serializer = AnswerOptionSerializer(answer, many=True)
        return Response({
            'Вопрос': question_serializer.data,
            'Ответ': answer_serializer.data
        })

    @staticmethod
    def put(request, pk):
        question_object = get_object_or_404(Question.objects.all(), pk=pk)
        serializer = QuestionSerializer(instance=question_object, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            question_object = serializer.save()
            return Response(f'Вопрос *{question_object}* успешно обновлен')

    @staticmethod
    def delete(request, pk):
        question_object = get_object_or_404(Question.objects.all(), pk=pk)
        question_object.delete()
        return Response(f'Опрос *{question_object}* был удален', status=204)


class AnswerOptionView(APIView):
    permission_classes = (IsGetOrIsAuthenticated, AdminPermission,)

    @staticmethod
    def get(request):
        answer = AnswerOption.objects.all()
        serializer = AnswerOptionSerializer(answer, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = AnswerOptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            answer_object = serializer.save()
            return Response(f'Вариант ответа *{answer_object}* успешно создан')


class AnswerOptionDetailsView(APIView):
    permission_classes = (IsGetOrIsAuthenticated, AdminPermission,)

    @staticmethod
    def get(request, pk):
        answer_object = get_object_or_404(AnswerOption.objects.all(), pk=pk)
        answer_serializer = AnswerOptionSerializer(answer_object)
        question_object = Question.objects.filter(id=pk)
        question_serializer = OneQuestionSerializer(question_object, many=True)
        return Response({
            'Вопрос': question_serializer.data,
            'Вариант ответа': answer_serializer.data,
        })

    @staticmethod
    def put(request, pk):
        answer_object = get_object_or_404(AnswerOption.objects.all(), pk=pk)
        serializer = AnswerOptionSerializer(instance=answer_object, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            answer_object = serializer.save()
            return Response(f'Вариант ответа *{answer_object}* успешно изменен')

    @staticmethod
    def delete(request, pk):
        answer_object = get_object_or_404(AnswerOption.objects.all(), pk=pk)
        answer_object.delete()
        return Response(f'Вариант ответа *{answer_object}* был удален', status=204)


class UserResponseView(APIView):
    permission_classes = (IsGetOrIsAuthenticated,)

    @staticmethod
    def get(request):
        response = UserResponse.objects.all()
        serializer = UserResponseSerializer(response, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = UserResponseSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            response_object = serializer.save()
            return Response(f'Ответ пользователя *{response_object}* успешно создан')


class UserResponseDetailsView(APIView):
    permission_classes = (IsGetOrIsAuthenticated,)

    @staticmethod
    def get(request, pk):
        response_object = get_object_or_404(UserResponse.objects.all(), pk=pk)
        response_serializer = OneUserResponseSerializer(response_object)
        return Response({'Вариант ответа': response_serializer.data})


class UserView(APIView):
    @staticmethod
    def get(request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            user_object = serializer.save()
            return Response(f'Пользователь *{user_object}* успешно создан')


class UserDetailsView(APIView):
    @staticmethod
    def get(request, pk):
        user_object = get_object_or_404(User.objects.all(), pk=pk)
        user_serializer = UserSerializer(user_object)
        return Response({'Пользователь': user_serializer.data})

    @staticmethod
    def put(request, pk):
        user_object = get_object_or_404(User.objects.all(), pk=pk)
        serializer = UserSerializer(instance=user_object, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_object = serializer.save()
            return Response(f'Данные пользователя *{user_object}* успешно обновлены')

    @staticmethod
    def delete(request, pk):
        user_object = get_object_or_404(User.objects.all(), pk=pk)
        user_object.delete()
        return Response(f'Пользователь *{user_object}* был удален', status=204)


class RegisterView(APIView):
    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    @staticmethod
    def post(request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Пользователь не найден')
        if not user.check_password(password):
            raise AuthenticationFailed('Некорректный пароль')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', 'HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserRegisterView(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('Неаутентифицированный!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Неаутентифицированный!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = RegisterSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    @staticmethod
    def post(request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Успешно!'
        }
        return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Пароль успешно изменен!'}, status=status.HTTP_200_OK)
            return Response({'error': 'Неверный старый пароль!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordReset(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        user = User.objects.filter(email__iexact=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()
            reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"
            send_mail(html=reset_url, text='Вот ваш токен сброса пароля', subject='Токен сброса пароля', from_email='',
                      to_emails=[''])
            return Response({'success': 'Мы отправили вам ссылку для сброса пароля'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Пользователь с учетными данными не найден"}, status=status.HTTP_404_NOT_FOUND)


class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        if new_password != confirm_password:
            return Response({"error": "Пароли не совпадают"}, status=400)
        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error': 'Недействительный токен'}, status=400)
        user = User.objects.filter(email=reset_obj.email).first()
        if user:
            user.set_password(request.data['new_password'])
            user.save()
            reset_obj.delete()
            return Response({'success': 'Пароль обновлен'})
        else:
            return Response({'error': 'Пользователь не найден'}, status=404)
