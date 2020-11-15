from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('comments/', views.comments),
    path('sentiments/', views.sentiments),
    path('commentNum/', views.CommentNumChartView.as_view()),
    path('chartJson/', views.ChartJsonView.as_view(), name='chart_params'),
]
