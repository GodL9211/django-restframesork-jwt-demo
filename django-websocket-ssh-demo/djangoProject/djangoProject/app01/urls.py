#! -*-conding=: UTF-8 -*-
# 2023/5/4 15:17

from django.contrib import admin
from django.urls import path
from app01.views import *


urlpatterns = [
    path('', webterminal),
]
