"""
使用 pandas 和 django ORM 处理数据
"""


from django.shortcuts import render
from django_pandas.io import read_frame
from .models import Smartphones
from .utils import process_data


def index(request):
    return render(request, 'index.html')


def comments(request):
    data = Smartphones.objects.all()
    return render(request, 'comments.html', locals())


def search_comment(request):
    comment_keyword = request.GET['comment_keyword']
    data = Smartphones.objects.filter(comment__icontains=comment_keyword)
    return render(request, 'comments.html', locals())


def search_date(request):
    date_keyword = request.GET['date_keyword']
    data = Smartphones.objects.filter(date__icontains=date_keyword)
    return render(request, 'comments.html', locals())


def analysis(request):
    queryset = Smartphones.objects.all()
    dataframe = read_frame(queryset)
    data = process_data(dataframe)
    return render(request, 'analysis.html', data)
