from rest_framework import serializers

from .models import (
    Survey,
    Question,
    AnswerOption,
    UserResponse,
    User
)


class SurveySerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    class Meta:
        model = Survey
        fields = ['title', 'description', 'start_date', 'end_date', 'is_active']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['survey', 'text', 'question_type']


class OneQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_type', 'text']


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['question', 'text']


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['question', 'selected_option', 'text_response', 'user_id']


class OneUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['text_response']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={
            'invalid': ('Пароль должен содержать не менее 8 символов,'
                        'а также содержать хотя бы одну заглавную букву и символ')
        })
    confirm_password = serializers.CharField(write_only=True, required=True)
