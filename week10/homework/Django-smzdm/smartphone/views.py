"""
使用 pandas 和 django ORM 处理数据
"""


import pandas as pd
from sqlalchemy import create_engine
from django.shortcuts import render
from django.conf import settings
from .models import Smartphones
from .process import process_data


user = settings.MYSQL_USER
pwd = settings.MYSQL_PWD
host = settings.MYSQL_HOST
database = settings.MYSQL_DB

engine = create_engine(
    f'mysql+pymysql://{user}:{pwd}@{host}/{database}')
rawdata = pd.read_sql_table('smartphones', engine, index_col='id')


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
    data = process_data(rawdata)
    return render(request, 'analysis.html', data)
