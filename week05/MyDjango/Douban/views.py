from django.shortcuts import render


def movie_reviews(request):
    return render(request, 'index.html')
