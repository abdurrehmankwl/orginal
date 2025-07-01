from django.contrib import admin
from django.urls import path ,include
from . import views

urlpatterns = [
    path('', views.detection_view, name='detection'),
]
