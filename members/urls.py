from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from . import views


urlpatterns = [
    path('login_user',views.login_user,name='logina')

]