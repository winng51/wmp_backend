"""wmp_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from topic_square.views import *
from mini_shop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('topic-square/labels', get_labels),
    path('topic-square/homework', get_homework_list),
    path('topic-square/topics', get_topics),
    path('topic-square/topic', get_topic),
    path('mini-shop/goods', get_goods),
    path('topic-square/login', open_id_login),
    path('topic-square/identity', identity),
]
