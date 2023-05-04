#! -*-conding=: UTF-8 -*-
# 2023/3/30 17:55

from rest_framework import routers
from django.urls import include, path
from common import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)

app_name = 'common'

urlpatterns = [
    path('', include(router.urls)),
]


if __name__ == '__main__':
    pass
