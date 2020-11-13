from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('comments/', views.comments),
    path('analysis/', views.analysis),
]
