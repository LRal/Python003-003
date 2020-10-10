from django.shortcuts import render
from .models import TenetReviews


def tenet_reviews(request):
    q = request.GET['q']
    print(q)
    # data = TenetReviews.objects.filter(star_rating__gt=3)
    data = TenetReviews.objects.filter(short_comment__icontains=q)
    return render(request, 'tenet.html', locals())
