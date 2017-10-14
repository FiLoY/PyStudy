"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import testing_view, book_view, test_process_view, test_sandbox_view, user_rating_view

urlpatterns = [
    url(r'^course/$', book_view, name='book_view'),
    url(r'^course/(?P<default_chapter_id>[0-9]+)/$', book_view, name='book_view'),

    url(r'^test/(?P<test_number>[0-9]+)/$', testing_view, name='testing_view'),
    # url(r'^question/$', question_view, name='question_view'),
    url(r'^test_process/$', test_process_view, name='test_process_view'),

    url(r'^sandbox/$', test_sandbox_view, name='test_sandbox_view'),

    url(r'^rating/$', user_rating_view, name='user_rating_view'),

    url(r'^', book_view, name='book_view'),

]
