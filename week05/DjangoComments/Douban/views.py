from django.shortcuts import render
from .models import TenetReviews


def tenet_reviews(request):
    tenet_data = TenetReviews.objects.filter(star_rating__gt=3)
    return render(request, 'index.html', locals())

def search(request, keyword):
    tenet_data = TenetReviews.objects.filter(short_comment__icontains=keyword)
    return render(request, 'index.html', locals())
