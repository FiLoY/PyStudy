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
from .views import login_view, logout_view, signup_view, settings_view, notifications_view, statistics_view


urlpatterns = [
    url(r'^login/$', login_view, name='login_view'),
    url(r'^logout/$', logout_view, name='logout_view'),
    url(r'^signup/$', signup_view, name='signup_view'),

    url(r'^settings/$', settings_view, name='settings_view'),
    url(r'^notifications/$', notifications_view, name='notifications_view'),
    url(r'^statistics/$', statistics_view, name='statistics_view'),

    url(r'^', login_view, name='login_view'),

]
