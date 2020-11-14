from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('comments/', views.comments),
    path('sentiments/', views.sentiments),
    path('chart/', views.CommentNumChartView.as_view()),
    path('chartJSON/', views.ChartParamsView.as_view(), name='chart_params'),
]
