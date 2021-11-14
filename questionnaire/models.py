from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=55, verbose_name='Название опроса')
    start_date = models.DateTimeField(verbose_name='Дата старта', auto_now_add=True, editable=False)
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.quiz_name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Опрос')
    question_text = models.TextField(blank=False, null=False, verbose_name='Текст вопроса')
    QUESTION_TYPES = (
        (1, 'Ответ текстом'),
        (2, 'Ответ с выбором одного варианта'),
        (3, 'Ответ с выбором нескольких вариантов'),
    )
    question_type = models.IntegerField(verbose_name='Тип вопроса', choices=QUESTION_TYPES)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer_text = models.CharField(max_length=255, verbose_name='Ответ текстом')

    def __str__(self):
        return self.answer_text

    def save(self, *args, **kwargs):
        if Question.objects.get(id=self.question.id).question_type == 1:
            raise ValidationError('У данного вопроса не может быть вариантов ответа')
        else:
            super(Answer, self).save(*args, **kwargs)


class Result(models.Model):
    user_id = models.IntegerField(verbose_name='Иденификаионный номер пользователя')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, verbose_name='Вопрос', null=True)
    chosen_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, verbose_name='Выбранный ответ',
                                      null=True, blank=True)
    written_answer = models.TextField(verbose_name='Текст ответа', null=True, blank=True)

    def __str__(self):
        if self.chosen_answer is None:
            answer = self.written_answer
        else:
            answer = self.chosen_answer
        return '{} - {}'.format(self.user_id, answer)

    def save(self, *args, **kwargs):
        if self.written_answer is None and self.chosen_answer is None:
            raise ValidationError('Необходимо дать какой то ответ')

        if Question.objects.get(id=self.question.id).question_type == 1:
            if self.written_answer is None:
                raise ValidationError('Необходимо написать свой ответ')

        if Question.objects.get(id=self.question.id).question_type == 2:
            if self.written_answer is not None or self.chosen_answer is None:
                raise ValidationError('Необходимо выбрать из предложенных вариантов')
            if Result.objects.filter(question=self.question, user_id=self.user_id).exists():
                raise ValidationError('У данного вопроса должен быть только один ответ')
            if not Answer.objects.filter(question=self.question, id=self.chosen_answer.id).exists():
                raise ValidationError('У данного вопроса нет такого ответа')

        if Question.objects.get(id=self.question.id).question_type == 3:
            if self.written_answer is not None or self.chosen_answer is None:
                raise ValidationError('Необходимо выбрать из предложенных вариантов')
            if Result.objects.filter(question=self.question, user_id=self.user_id, chosen_answer=self.chosen_answer).exists():
                raise ValidationError('Вы уже давали на этот вопрос такой ответ')
            if not Answer.objects.filter(question=self.question, id=self.chosen_answer.id).exists():
                raise ValidationError('У данного вопроса нет такого ответа')
        super(Result, self).save(*args, **kwargs)

