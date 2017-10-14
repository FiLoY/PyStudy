from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.utils import http


def login_view(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        title = 'PyStudy - Аутентификация'
        template = 'account/log_in.html'
        context = {'title': title, }

        redirect_to = request.POST.get('next', request.GET.get('next', '/'))
        redirect_to = (redirect_to if http.is_safe_url(redirect_to, request.get_host()) else '/')
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect(redirect_to)
                    else:
                        form.add_error('username', 'Данный пользователь был удален.')
                else:
                    form.add_error('username', 'Данный пользователь не найден или неверный пароль.')
        else:
            form = LoginForm()

        context['form'] = form
        context['next'] = request.GET.get('next') or ''
        return render(request, template, context)


def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        title = 'PyStudy - Регистрация'
        template = 'account/sign_up.html'
        context = {'title': title, }

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request, user)
                return redirect('/')
        else:
            form = SignUpForm()

        context['form'] = form
        return render(request, template, context)


def password_reset_view(request):
    pass


def settings_view(request):
    if not request.user.is_authenticated():
        return redirect('/')
    else:
        title = 'PyStudy - Настройки'
        template = 'account/user_main_settings.html'
        context = {
            'title': title,
            'user': request.user,
            'active': 'active',
            'url_name': 'settings_view',
        }

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
        else:
            form = ProfileForm(initial={'username': request.user.username,
                                        'email': request.user.email,
                                        'first_name': request.user.first_name,
                                        'second_name': request.user.second_name,
                                        'last_name': request.user.last_name,
                                        'date_of_birth': request.user.date_of_birth,
                                        })

        context['form'] = form
        return render(request, template, context)


def notifications_view(request):
    if not request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == 'POST':
            pass
        else:
            pass
        title = 'PyStudy - Уведомления'
        template = 'account/user_notifications_settings.html'
        context = {
            'title': title,
            'user': request.user,
            'active': 'active',
            'url_name': 'notifications_view',
        }
        return render(request, template, context)


def statistics_view(request):
    if not request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == 'POST':
            pass
        else:
            pass
        title = 'PyStudy - Статистика'
        template = 'account/user_statistics.html'
        context = {
            'title': title,
            'user': request.user,
            'active': 'active',
            'url_name': 'statistics_view',
        }
        return render(request, template, context)
