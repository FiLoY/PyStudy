from django.shortcuts import render, redirect, HttpResponse
from .models import LevelOfComplexity, Question, Answer, Chapter, UserChapter, Test, UserTest, QuestionTestDone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
import random
from django.views.decorators.csrf import csrf_exempt
from apps.account.models import User


@csrf_exempt
@login_required
def test_process_view(request):
    context = {}
    json_data = {}
    if 'test-id' in request.POST:
        test = Test.objects.get(pk=request.POST['test-id'])
        user = request.user
        all_questions_of_this_test = list(test.question_set.all())
        secure_random = random.SystemRandom()
        secure_random.shuffle(all_questions_of_this_test)
        # Активируем тест пользователя
        starting_user_test = UserTest(test=test, user=user)
        starting_user_test.start_time = timezone.now()
        starting_user_test.save()
        # Добавляем ему все вопросы
        for i in range(test.max_questions):
            user_test_question = QuestionTestDone()
            user_test_question.user_test = starting_user_test
            user_test_question.question = all_questions_of_this_test[i]
            user_test_question.save()
        context['test'] = starting_user_test.test
        context['user_test_id'] = starting_user_test.id
        context['question'] = starting_user_test.questiontestdone_set.first().question
        context['question_id'] = starting_user_test.questiontestdone_set.first().id
        shuffle_answers = list(starting_user_test.questiontestdone_set.first().question.answer_set.all())
        secure_random = random.SystemRandom()
        secure_random.shuffle(shuffle_answers)
        context['answers'] = shuffle_answers
        QuestionTestDone.objects.filter(pk=starting_user_test.questiontestdone_set.first().id).update(viewed=True)
    else:
        user_test = UserTest.objects.get(pk=request.POST['user-test-id'])
        context['test'] = user_test.test
        context['user_test_id'] = request.POST['user-test-id']
        all_questions_of_this_test = list(user_test.questiontestdone_set.all())
        for item in all_questions_of_this_test:
            if not item.viewed:
                context['question'] = item.question
                context['question_id'] = item.id
                QuestionTestDone.objects.filter(pk=item.id).update(viewed=True)
                shuffle_answers = list(item.question.answer_set.all())
                secure_random = random.SystemRandom()
                secure_random.shuffle(shuffle_answers)
                context['answers'] = shuffle_answers
                UserTest.objects.filter(pk=user_test.id).update(date_of_done=timezone.now())
                break
        # Высчитываем отвпеты балы и т д! ТЕст Выполнен!
        if 'question' not in context:
            UserTest.objects.filter(pk=user_test.id).update(date_of_done=timezone.now())
            context['user_test'] = user_test
            context['time_done'] = user_test.date_of_done - user_test.start_time
            context['true_answers'] = user_test.true_answers()
            json_data['done'] = render_to_string('education/test_done.html', context)

    if 'answer_id' in request.POST and 'question_id' in request.POST:
        QuestionTestDone.objects.filter(pk=request.POST['question_id']).update(answer_id=request.POST['answer_id'])
    template = 'education/form_question.html'
    html = render_to_string(template, context)
    json_data['code'] = html
    return JsonResponse(json_data)

#
# @login_required
# def question_view(request):
#     title = 'PyStudy - '
#     print('fhsdfjkgfskdjgsdfkjghrebdsjkfvbriu')
#     template_testing = 'education/form_question.html'
#     context = {
#         'title': title,
#     }
#     return render(request, template_testing, context)


@login_required
def testing_view(request, test_number):
    test = Test.objects.get(pk=test_number) # текущий тест
    user_tests = UserTest.objects.all().filter(test=test, user=request.user) # все попытки пройти текущий тест
    # последний пройденный тест
    last_test = ''
    if user_tests:
        last_test = user_tests.order_by('id').last()

    title = 'PyStudy - ' + test.name # название странички
    template = 'education/test_page.html' # шаблон странички

    context = {
        'title': title,
        'test': test,
        'last_test': last_test,
        'user_tests_count': user_tests.count(),
    }

    return render(request, template, context)


# book view with chapters
@login_required
def book_view(request, default_chapter_id=Chapter.objects.all().order_by('_order').first().id):
    title = 'PyStudy - Учебник' # название странички
    template = 'education/book.html' # шаблон странички
    user = request.user # текущий пользователь

    chapters = Chapter.objects.all().order_by('_order') # список глав учебника
    correct_chapter = chapters.get(pk=default_chapter_id) # текущая глава учебника

    correct_chapter.mark_chapter_as_read(user=user) # Отметка прочитанной главы, начисление опыта пользователю

    # Утрамбовка полученых данных
    context = {
        'title': title,
        'chapters': chapters,
        'correct_chapter': correct_chapter,
    }
    return render(request, template, context)


# all tests
@login_required
def test_sandbox_view(request):
    title = 'PyStudy - Песочница тестов' # название странички
    template = 'education/test_sandbox.html' # шаблон странички

    tests = Test.objects.all() # список всех тестов

    context = {
        'title': title,
        'tests': tests,
    }
    return render(request, template, context)


# users rating
@login_required
def user_rating_view(request):
    title = 'PyStudy - Рейтинг пользователей' # название странички
    template = 'education/user_rating.html' # шаблон странички

    users = User.objects.all().order_by('-experience')[:15] # список первых 15 пользователей по опыту

    context = {
        'title': title,
        'users': users,
    }
    return render(request, template, context)
