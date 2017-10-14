from django.db import models
from django.utils import timezone
from apps.account.models import User
from datetime import time
from django.core.exceptions import ObjectDoesNotExist


# ---------------------------
# Уровень пользователей     -
# ---------------------------
class UserLevel(models.Model):
    """
        Model for user's level
    """
    class Meta:
        db_table = 'education_user_level'
        app_label = 'education'
    level = models.IntegerField(verbose_name='level', default=0)
    experience_start_range = models.IntegerField(verbose_name='experience start range', default=0)
    experience_end_range = models.IntegerField(verbose_name='experience end range', default=0)
    # color = models.CharField(verbose_name='color', max_length=10, default='#ffffff')


# ---------------------------
# Уровни тестов             -
# ---------------------------
class LevelOfComplexity(models.Model):
    class Meta:
        db_table = 'education_level_of_complexity'
    name = models.CharField(verbose_name='name', max_length=35, blank=True, default='')
    level = models.IntegerField(verbose_name='level', default=0)
    lite_description = models.TextField(verbose_name='lite description', blank=True, default='')
    full_description = models.TextField(verbose_name='full description', blank=True, default='')
    normal_experience = models.IntegerField(verbose_name='normal experience', default=0)
    extra_experience = models.IntegerField(verbose_name='extra experience', default=0)


# ---------------------------
# Учебники                  -
# ---------------------------
class Book(models.Model):
    class Meta:
        db_table = 'education_book'
    name = models.CharField(verbose_name='book name', max_length=50)
    description = models.TextField(verbose_name='description', blank=True, default='')
    date_of_create = models.DateTimeField(verbose_name='date of create', default=timezone.now)


# ---------------------------
# Учебник по главам         -
# ---------------------------
class Chapter(models.Model):
    class Meta:
        db_table = 'education_book_chapter'
        order_with_respect_to = 'book'
    book = models.ForeignKey(Book)
    name = models.CharField(verbose_name='chapter name', max_length=50)
    text = models.TextField(verbose_name='chapter text')
    experience = models.IntegerField(verbose_name='normal experience', default=0)
    users = models.ManyToManyField(User, through='UserChapter')
    date_of_create = models.DateTimeField(verbose_name='date of create', default=timezone.now)

    # Получение теста главы, если он есть
    def get_chapter_test_or_none(self):
        try:
            test = self.test_set.get()
        except ObjectDoesNotExist:
            test = None
        return test

    # Получение id предыдущей главы, если она есть
    def get_previous_chapter_id_or_none(self):
        try:
            previous_chapter_id = self.get_previous_in_order().id
        except ObjectDoesNotExist:
            previous_chapter_id = None
        return previous_chapter_id

    # Получение id следующей главы, если она есть
    def get_next_chapter_id_or_none(self):
        try:
            next_chapter_id = self.get_next_in_order().id
        except ObjectDoesNotExist:
            next_chapter_id = None
        return next_chapter_id

    def mark_chapter_as_read(self, user):
        try:
            UserChapter.objects.get(user=user, chapter=self)
        except ObjectDoesNotExist:
            UserChapter(user=user, chapter=self).save()
            user.experience += self.experience
            user.save()


# ----------------------------------------
# Связь учебника с пользователем         -
# ----------------------------------------
class UserChapter(models.Model):
    class Meta:
        db_table = 'education_user_chapter'
    user = models.ForeignKey(User)
    chapter = models.ForeignKey(Chapter)
    date_of_reading = models.DateTimeField(verbose_name='date of reading', default=timezone.now)


# ---------------------------
# Сущность теста            -
# ---------------------------
class Test(models.Model):
    class Meta:
        db_table = 'education_test'
    chapter = models.ForeignKey(Chapter, null=True)
    name = models.CharField(verbose_name='test name', max_length=50)
    description = models.TextField(verbose_name='description', blank=True, default='')
    experience = models.IntegerField(verbose_name='experience', default=0)
    time = models.TimeField(verbose_name='time', default=time(0, 15, 0))
    users = models.ManyToManyField(User, through='UserTest')
    date_of_create = models.DateTimeField(verbose_name='date of create', default=timezone.now)
    max_questions = models.IntegerField(verbose_name='maximum of questions', default=0)

    def max_experience(self):
        max_exp = self.experience
        for question in self.question_set.all():
            max_exp += question.experience
        return max_exp

    # def number_of_questions(self):
    #     return self.question_set.all().count()


# ----------------------------------------
# Связь теста с пользователем            -
# ----------------------------------------
class UserTest(models.Model):
    class Meta:
        db_table = 'education_user_test'
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    start_time = models.DateTimeField(verbose_name='start time', default=timezone.now)
    date_of_done = models.DateTimeField(verbose_name='date of done', default=timezone.now)

    def true_answers(self):
        true_an = 0
        for item in self.questiontestdone_set.all():
            if item.answer:
                if item.answer.is_true:
                    true_an = true_an + 1
        return true_an

    def test_time_done(self):
        return str(self.date_of_done - self.start_time)[:-7]


# ---------------------------
# Вопросы к тесту           -
# ---------------------------
class Question(models.Model):
    class Meta:
        db_table = 'education_question'
    chapter = models.ForeignKey(Chapter)
    tests = models.ManyToManyField(Test)
    user_test_question_done = models.ManyToManyField(UserTest, through='QuestionTestDone')
    text = models.TextField(verbose_name='question text', blank=True)
    experience = models.IntegerField(verbose_name='experience', default=0)


# ---------------------------
# Ответы к вопросам теста   -
# ---------------------------
class Answer(models.Model):
    class Meta:
        db_table = 'education_answer_to_question'
    question = models.ForeignKey(Question)
    text = models.CharField(verbose_name='answer to question', max_length=35, blank=True)
    is_true = models.BooleanField()


# ----------------------------------
# как решена задача в тесте        -
# ----------------------------------
class QuestionTestDone(models.Model):
    class Meta:
        db_table = 'education_question_test_done'
    user_test = models.ForeignKey(UserTest)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer, null=True)
    viewed = models.BooleanField(verbose_name='question viewed', default=False)
