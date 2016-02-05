# coding: utf-8
from django.conf.urls import url, patterns
from core import views

urlpatterns = [
    url(r'^$', views.index),
]