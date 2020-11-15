"""
将 Django ORM 的 QuerySet 转换成 Pandas 的 DataFrame 类型, 以更便捷地处理数据
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django_pandas.io import read_frame
from .models import Smartphones
from .process_data import df_to_json, analyse_sentiments, get_chart_params


QS = Smartphones.objects.all()
DF = read_frame(QS)


def index(request):
    """首页"""

    return render(request, 'index.html')


def comments(request):
    """
    评论数据展示页
    展示内容：ID、产品名称、日期、评论内容、舆情数据
    支持功能：分页、高级搜索、排序、细节展示、选取列
    """

    data = df_to_json(DF)
    return render(request, 'comments.html', data)


def sentiments(request):
    """
    舆情数据分析页
    展示内容：各产品评论总数、积极评论数量、积极评论比例
    支持功能：搜索、排序、选取列
    """

    data = analyse_sentiments(DF)
    return render(request, 'sentiments.html', data)


class CommentNumChartView(TemplateView):
    """
    评论数量趋势页
    展示内容: 以线形图形式展示双十一活动期间 (10/21-11/10), 各产品每日评论数量
    支持功能: 筛选产品、显示数据
    """

    template_name = 'comment_num.html'


class ChartJsonView(BaseLineChartView):
    """以 .json 格式储存线形图数据"""

    param_list = get_chart_params(DF)

    def get_labels(self):
        """横坐标 (日期) """
        return self.param_list[0]

    def get_providers(self):
        """数据集 (品名) """
        return self.param_list[1]

    def get_data(self):
        """纵坐标 (评论数) """
        return self.param_list[2]
