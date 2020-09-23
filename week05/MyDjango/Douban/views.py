from django.shortcuts import render
from .models import MovieReviews


def movie_reviews(request):
    data = MovieReviews.objects.filter(n_star__gt=3)
    return render(request, 'index.html', locals())
