from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .form import LoginForm


def index(request):
    return HttpResponse("欢迎来到首页")


def login_(request):
    # POST
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 如果表单信息符合 LoginForm 里的格式
            # auth 验证
            cleaned_data = login_form.cleaned_data
            user = authenticate(
                username=cleaned_data['username'],
                password=cleaned_data['password']
            )
            if user:  # auth 验证成功
                login(request, user)
                return redirect('http://localhost:8000/')
            else:
                return HttpResponse('密码错误')
    # GET
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'form.html', {'form': login_form})
