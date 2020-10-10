from django.urls import path, re_path
from . import views

urlpatterns = [
    path('tenet', views.tenet_reviews),
]