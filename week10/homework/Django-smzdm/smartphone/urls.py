from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('comments/', views.comments),
    path('comments/search_comment', views.search_comment),
    path('comments/search_date', views.search_date),
    path('analysis/', views.analysis),
]
