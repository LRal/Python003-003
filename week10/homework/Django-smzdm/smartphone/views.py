"""
使用 pandas 和 django ORM 处理数据
"""

from django.shortcuts import render
from django_pandas.io import read_frame
from .models import Smartphones
from .utils import process_data, df_to_json


def index(request):
    return render(request, 'index.html')


def comments(request):
    queryset = Smartphones.objects.all()
    dataframe = read_frame(queryset)
    data = df_to_json(dataframe)
    return render(request, 'comments.html', data)


def analysis(request):
    queryset = Smartphones.objects.all()
    dataframe = read_frame(queryset)
    data = process_data(dataframe)
    return render(request, 'analysis.html', data)
