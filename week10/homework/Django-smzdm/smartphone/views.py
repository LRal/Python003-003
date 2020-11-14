"""
使用 pandas 配合 Django ORM 处理数据
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django_pandas.io import read_frame
from .models import Smartphones
from .utils import analyse_sentiments, df_to_json, get_chart_params

queryset = Smartphones.objects.all()
dataframe = read_frame(queryset)


def index(request):
    return render(request, 'index.html')


def comments(request):
    data = df_to_json(dataframe)
    return render(request, 'comments.html', data)


def sentiments(request):
    data = analyse_sentiments(dataframe)
    return render(request, 'sentiments.html', data)


class LineChartJSONView(BaseLineChartView):
    processd_list = get_chart_params(dataframe)

    def get_labels(self):
        return self.processd_list[0]

    def get_providers(self):
        return self.processd_list[1]

    def get_data(self):
        return self.processd_list[2]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()
