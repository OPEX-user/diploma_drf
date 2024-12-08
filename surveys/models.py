from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    STATUS = (
        ('active', 'активный'),
        ('inactive', 'неактивный'),
    )

    id = models.IntegerField(
        verbose_name='ID',
        primary_key=True,
        unique=True,
        auto_created=True)
    title = models.CharField(verbose_name='Название', max_length=50, null=False)
    description = models.TextField(verbose_name='Описание', null=True)
    start_date = models.DateTimeField(verbose_name='Дата начала', null=False, auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='Дата окончания', null=True)
    is_active = models.CharField(verbose_name='Статус активности опроса', max_length=20, choices=STATUS, null=False)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    ONLY_CHOICE = 'OC'
    MULTIPLE_CHOICES = 'MC'
    TEXT = 'TX'
    QUESTION_TYPES = (
        (ONLY_CHOICE, 'Выбор одного варианта'),
        (MULTIPLE_CHOICES, 'Выбор нескольких вариантов'),
        (TEXT, 'Ответ текстом'),
    )

    id = models.IntegerField(
        verbose_name='ID',
        primary_key=True,
        unique=True,
        auto_created=True)
    survey = models.ForeignKey(to='Survey', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Текст вопроса', null=False)
    question_type = models.CharField(verbose_name='Тип вопроса', max_length=50, choices=QUESTION_TYPES)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerOption(models.Model):
    id = models.IntegerField(
        verbose_name='ID',
        primary_key=True,
        unique=True,
        auto_created=True)
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE, related_name='answer_options')
    text = models.TextField(verbose_name='Текст варианта ответа', null=False)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class UserResponse(models.Model):
    id = models.IntegerField(
        verbose_name='ID',
        primary_key=True,
        unique=True,
        auto_created=True)
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE, related_name='question_responses')
    selected_option = models.ForeignKey(to='AnswerOption', on_delete=models.CASCADE, related_name='option_responses')
    text_response = models.TextField(verbose_name='Текстовый ответ пользователя', null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return f"{self.text_response}"

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
