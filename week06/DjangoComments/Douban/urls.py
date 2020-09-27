from django.urls import path
from . import views

urlpatterns = [
    path('tenet', views.tenet_reviews),
    # path('tenet/search', views.search, name='search'),
]
