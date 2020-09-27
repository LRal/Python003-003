from django.shortcuts import render
from .models import TenetReviews


# def tenet_reviews(request):
#     data = TenetReviews.objects.all()
#     q = request.GET['q']
#     return render(request, 'tenet.html', locals())

# 这段代码也是 raise MultiValueDictKeyError
# def search(request):
#     q = request.GET['q']
#     data = TenetReviews.objects.filter(short_comment__icontains=q)
#     return render(request, 'tenet.html', locals())

def tenet_reviews(request):
    data = TenetReviews.objects.filter(star_rating__gt=3)
    return render(request, 'tenet.html', locals())