# Django 相关功能

## 管理员界面

管理员界面可以帮助管理员管理信息

### 创建管理员账号

`python manage.py createsuperuser`

### 设置管理员账户可查看的信息

```python
# ./<app>/admin.py
from django.contrib import admin
from .models import <database>  # 需要先做好数据转移工作

admin.site.register(<database>)  # 将数据表信息注册到管理员页面

```

### 注意事项

1. 需要先 `python manage.py makemigrations`, 在数据库中做好相应的准备工作

## 表单管理

### HTML 的表单

```html
<form action="result.html" method="post">
username:<input type="text" name="username" /> <br>
password:<input type="password" name="password" /> <br>
<input type="submit" value="登录">
</form>
```

### Django 中的表单

在 Django 中, 可以选择使用 Python 语言来写表单
表单url - view视图 - 表单 - django-html

```python
# ./<app>/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_),
]
```

```python
# ./<app>/form.py
# 这个也可以写在 views.py 中, 但单独弄一个 form.py 会让代码可读性更佳
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
```

```python
# ./<app>/views.py
from django.shortcuts import render
from .form import LoginForm

def login_(request):
    # GET
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'form.html', {'form': login_form})
```

```html
<form action="/login" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Login">
</form>
```

## 用户管理认证

### 创建用户

第一步: `python manage.py shell`

第二步:

```python
from django.contrib.auth.models import user
from django.contrib.auth import authenticate, login

# 创建用户
user = User.objects.create_user('username', 'email', 'password')
user.save()

# 进行 auth 验证
user = authenticate(username='username', password='password')
user  # 如果验证成功, 会输出账号信息; 否则, 输出为空
```

> 也可以直接从管理员页面创建账号, 操作更简单

### 把 auth 验证应用到 views 中

```python
# ./<app>/views.py
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .form import LoginForm

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
                return HttpResponse('登录成功')
            else:
                return HttpResponse('登陆失败')
```

## 信号和中间件

### 信号

```python
# ./<app>/views.py
from django.core.signals import request_started
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_started)
def started(sender, **kwargs):
    print("Request started!")

@receiver(request_finished)
def finished(sender, **kwargs):
    print("Request finished!")

# 当你发起了任意 request 之后, 输出效果示例
# Request started!
# [18/Oct/2020 08:12:05] "GET / HTTP/1.1" 200 18
# Request finished!
```

> 除了例子中的 request 信号, 还有 model signals, management signals 等等
> 详见[官方文档](https://docs.djangoproject.com/en/3.1/ref/signals/#signals)

### 中间件

中间件能让你在 request 和 response 之间进行操作, 如设置反爬虫

```python
# ./<app>/middleware.py
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class Middleware(MiddlewareMixin):
    """这些函数的名字和参数一般都是固定的"""
    def process_request(self, request):
        print('中间件请求')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('中间件视图')

    def process_exception(self, request, exception):
        print('中间件异常')

    def process_response(self, request, response):
        print('中间件响应')
        return response
```

```python
# ./<project>/settings.py
# 在设置中添加 Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'index.middleware.Middleware',  # 添加 Middleware
]
```

### request 信号和中间件的关系

request_started 信号 -> 中间件 -> request_finished 信号

## 生产环境

使用 gunicorn 让 Django 能够并发运行, 以应对多用户同时登陆的情况
使用方法非常简单, 只需要 `pip install gunicorn`
以后启动时使用 `gunicorn MyDjango.wsgi` 来代替 `python manage.py runserver` 即可

> gunicorn 是比 Nginx 更高效更便捷的库, 但是不支持在 windows 运行
