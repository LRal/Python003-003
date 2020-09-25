# Django 入门

## 框架概览

采用 MTV 框架模式

![MTV框架][mtv_url]

[mtv_url]: https://github.com/LRal/Pics/blob/master/MTV.png?raw=true

## 安装

`pip install django`

成功标志：终端能运行 django-admin 程序

## 配置项目

### 创建项目

`django-admin startproject <project>`

### 启动与关闭

首先要 cd 到项目目录下：

`cd <project>`

#### 启动服务器

`python manage.py runserver`

默认端口：127.0.0.1:8000  
可更改为：0.0.0.0:80，使其他电脑能连接到开发服务器  

#### 关闭服务器

`Ctrl + C`

关闭服务器保障了开发的安全。

## 配置 app

### 创建 app

`django-admin startapp <app>`  

App和项目的关系:一个项目是一个特定站点配置和App的集合;一个项目可以包含多个App,一个App可以存在于多个项目。

### 将 app 注册到 Django 中

```python
# <project> 下的 settings.py
INSTALLED_APPS = [
    'django.contrib.admin',  # 内置的后台管理系统
    'django.contrib.auth',  # 内置的用户认证系统
    'django.contrib.contenttypes',  # 所有model元数据
    'django.contrib.sessions',  # 会话，表示当前访问网站的用户身份
    'django.contrib.messages',  # 消息提示
    'django.contrib.staticfiles',  # 静态资源路径
    '<app>',  # 创建的 app
]
```

## 配置 SQL

### 配置数据库信息

```python
# <project> 下的 settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '666666',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
```

### 配置 Django 中数据库驱动

```python
# <project> 下的 __init__.py

import pymysql
pymysql.install_as_MySQLdb()
```

### 异常处理

#### 提示版本过低

提示：mysqlclient x.x.x or newer is required; you have y.y.y.

- 解决办法1：在 __init\__.py 中添加一行 `pymysql.version_info = (x, x, x, "final", 0)`，手动把版本调高
- 解决办法2：把引起报错的源码注释掉（不影响正常使用）

  ```python
  # 对应源码位置一般会在终端显示，类似这样：
  # if version < (1, 4, 0):
  # raise ImproperlyConfigured('mysqlclient 1.4.0 or newer is required; you have %s.' % Database.__version__)
  ```

## 路由层（URLConf）

URLconf，也称 URL 调度器、路由层，是命名为 urls.py 的文件。
可以理解为一份 URL 目录，里面包含 项目/app 下的各种 URL 模式及对应处理方式。
当接收到一个 request，Django 会依次匹配每个 URL 模式：
&emsp;如果匹配成功，就按照指向的函数去处理；
&emsp;如果匹配失败，就调用一个适当的错误处理视图（这个视图也是可以自定义的）。

### 项目下的 URLconf

<project\> 下的 urls.py。

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<app>/', include('<app>.urls')),  # 使用 include() 引用其他 app 下的 URLconf
]
```

#### path() 函数

用于解析 URL 地址，然后调用预先编写好的视图层（views.py）里的函数。

```python
path(route, view, kwargs=None, name=None)
# route: 表示端口以后的 URL 地址的模式。如果要用到正则表达式，那我们用 re_path() 代替 path() 即可。
# view: 表示 route 匹配成功后，需要调用视图层(views.py)的哪层函数
# kwargs: 若 URL 中带有多个变量（如下面的 name），可以作为一个字典传递给目标视图函数，如下所示：
    # def name(request, **kwargs):
    #     return HttpResponse(kwargs['name'])
# name: 为 URL 取名，使你在 Django 的任意地方唯一地引用它，尤其是在模板中。
```

### app 下的 URLconf

默认情况下，<app\> 下是没有 urls.py 的。
如果项目非常庞大，app 非常多，应用的 URL 都写在根 urls.py 配置文件中的话，会显的非常杂乱，还会出现名称冲突之类的问题。
因此我们一般会为每个 app 创建它们各自的 urls.py 配置文件，然后在根 urls.py 里用 include() 函数引用。

#### URLconf 是怎么调用视图层的

如果匹配到某个 URL 模式，URL 调度器会调用视图层的函数。

```python
# <app\> 下的 urls.py

from django.urls import path
from . import views  # 调用 app 的视图层 (views.py)

urlpatterns = [
    path('<route>', views.<index>)  # 如果匹配到 URL 模式，则调用视图层里的 index() 函数
]
```

```python
# <app\> 下的 views.py

from django.http import HttpResponse  # HttpResponse 是一种响应类型，后面会细讲

def <index>(request):  # 视图层里的 index() 函数
    return HttpResponse("Hello Django!")

# 视图层里的函数都要带 request 对象
```

### URL 规则（route）详解

如何写 path() 函数里的 route 参数？
主要有三种方式。

#### 带变量的 URL

Django 支持对 URL 设置变量，URL 变量类型包括：  

- str
- int
- slug
- uuid
- path

```python
path('<int:year>', views.func)  # 如 http://127.0.0.1:8000/2020
path('<int:year>/<str:name>', views.func)  # 如 http://127.0.0.1:8000/2020/hello

# 注意：当 URL 中包含两个或以上的变量时，对应的 func 要使用 kwargs 参数
```

#### 与正则表达式匹配的 URL

要使用正则表达式，用 re_path() 替换 path() 即可

```python
re_path('(?P<year>[0-9]{4}).html', views.func, name='urlyear')  # 如 http://127.0.0.1:8000/2020
# "?P<year>" 表示正则表达式中小括号内的变量名为 year
# name='urlyear' 中的 urlyear 会使用在模板中
# 这两个名字要注意区分
```

#### 自定义变量类型

有时候使用正则表达式会显得不够优雅，于是我们创建自定义过滤器，将变量类型与正则表达式结合。

```python
# 第一步：在 converters.py 中写转换类
# <app> 下的 converters.py （需自己创建）
class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):  # 必写的函数，声明你的 value 在 python 中是什么样的类型
        return int(value)

    def to_url(self, value):  # 必写的函数，声明你的 value 在 django 的 url 中是什么样的类型
        return '%04d' % value
```

```python
# 第二步：在 urls.py 中使用 register_converter 调用转换类，并声明数据类型，就可以使用 path() 解析了
# <app> 下的 urls.py
from django.urls import register_converter
register_converter(converters.FourDigitYearConverter, 'yyyy')
urlpatterns = [
    path('<yyyy:year>', views.year),
]
```

```python
# 第三步：在 views.py 中写对应的函数
# <app> 下的 views.py
def year(request, year):
    return HttpResponse(year)
```

## 视图层（views.py）

命名为 urls.py 的文件。
视图层的功能是接受匹配到的 URL 所带来的 request 并给出一个 response。
这个功能由我们自己编写的一个个**视图函数**来完成。
视图函数命名没有规定，必须带一个叫 request 的参数。
视图函数往往会和模型层、模板层进行交互。

### 响应类型

前面的 views.py 中，有一句`from django.http import HttpResponse`，这里的 HttpResponse 是一种响应类型。

HttpResponse 是 Django 中最基本的响应类型；
其他的响应类型可查阅[官方文档](https://docs.djangoproject.com/en/3.1/ref/request-response/#httpresponse-subclasses)。

### 快捷方式

对于一些响应类型，在 django 中会有对应的快捷函数。
常见的有 render(), redirect(), get_object_or_404() 等。

```python
from django.shortcuts import render, redirect

def func(request):
    """
    render() 通常用于需要模板的地方。
    它会把给定的变量传给 <app>/templates 下的模板，并返回一个 HttpResponse 对象。
    """
    var1 = '一个会在模板里用到的变量'
    var2 = '另一个也会在模板里用到的变量'
    return render(request, 'templates.html', locals())
# 这里的 templates.html 是模板，位于 <app>/templates 下（需自己创建文件夹）。
# locals() 函数会以字典类型返回当前位置的所有局部变量，在这里指的是 var1, var2。

def year(request, year):
    """
    redirect() 默认返回一个临时的重定向。
    参数 permanent=True 可返回一个永久的重定向。
    """
    return redirect('/2020.html')
```

## 模型层（ORM）

ORM(Object Relational Mapping)，对象-关系-映射，是 MTV 框架中一个重要的组成部分。
它是对数据库驱动（如 pymysql）的封装，让开发人员无需依赖特定的数据库，也不需要面对因数据库变更而导致的无效劳动。
ORM 对象的类型是 QuerySet, 这是一个类似字典的数据类型，因此除了 ORM 自身的方法（如 CRUD），它也支持一些 Python 的方法（如切片）。

### ORM 和 SQL 之间的数据转移

#### ORM 到 SQL

1. 创建用于数据迁移的 py 文件：`python manage.py makemigrations`
2. 数据迁移：`python manage.py migrate`

#### SQL 到 ORM

- 将 SQL 所有表迁移到 ORM 中
    `python manage.py inspectdb`
- 将上述语句的执行结果保存到 test.py 中
    `python manage.py inspectdb > test.py`
    test.py 位置在同级目录下生成。

### 数据类型及参数

[官方文档](https://docs.djangoproject.com/en/3.1/ref/models/fields/)

#### 常用数据类型

- **AutoField**
    int 自增列，必须填入参数 primary_key=True。
    如果不提供，**Django 会自动创建一个名为 id 的自增列**。
- **IntegerField**
    整数类型。
- **CharField**
    字符类型，必须提供 max_length 参数，max_length 表示字符长度。
- **DateField**
    日期类型，格式：YYYY-MM-DD。
- **DateTimeField**
    日期时间类型，格式：YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]。

#### 常用参数

- null
- unique
- primary_key
- max_length

### 创建数据表

想创建一个 Person 数据表，SQL 语句是这样的：

```MySQL
CREATE TABLE person (
"id" serial NOT NULL PRIMARY KEY,
"first_name" varchar(30) NOT NULL,
"last_name" varchar(30) NOT NULL
);
```

ORM 是这样的：

```python
# <app> 下的 models.py

from django.db import models

class Person(models.Model):  # 每个类都继承 models 模块的 Model 类
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

### CRUD

```python
# 虽然属于模型层，但增删查改一般写在 <app> 下的视图层（views.py）
# 以刚才创建的 Person 数据表为例

from index.models import *

# 增
Person.objects.create(first_name='John', last_name='Doe')
Person.objects.create(first_name='Yan', last_name='Jimmy')

# 查
Person.objects.get(id=2).first_name  # 返回一个 model 对象
# Person.objects.filter(id=2)  
# filter() 返回的是 QuerySet 对象，并不能真正地查询

# 改
Person.objects.filter(id=2).update(first_name='YAN')

# 删
Person.objects.filter(first_name='Yan').delete()  # 删除单条数据
Person.objects.all().delete()  # 删除全部数据
```

> 更多方法，参考[官方文档](https://docs.djangoproject.com/en/3.1/ref/models/querysets/)

## 模板层（Templates）

Django 有自己的一套 html 语言，可应用在 Templates 文件夹的 html 文件中。

### 常用语法

- **模板变量**
    {{ var }}
- **从 URL 获取模板变量**
    {% url 'var' 2020 %}
- **for 遍历标签**
    {% for type in type_list %}
    {% endfor %}
    > 通常结合 locals() 函数使用。
- **if 判断标签**
    {% if name.type==tpye.type %}
    {% endif %}
- **读取静态资源内容**
    {% static 'css/headers.css' %}

### 结合模板进行开发

1. 下载模板文件，放到 <app\>/static 目录下
2. 在 html 模板中 head 标签里加入下列语句，引入下载的 css, js 文件：

    ```js
    <head>
        {% load static %}

        {% block css %}
            <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        {% endblock %}

        {% block js %}
            <script src="{% static 'js/bootstrap.min.js' %}"></script>
            <script src="{% static 'js/jquery.slim.min.js' %}"></script>
        {% endblock %}
    </head>
    ```

### 应用举例：展示数据库中的内容

1. 经过 ORM 进行 CRUD 操作后，把 QuerySet 对象传进 html 模板中：

    ```python
    # <app> 下的 views.py
    def movie_reviews(request):
        movie_data = MovieReviews.objects.filter(n_star__gt=3)
        return render(request, 'index.html', locals())
    ```

2. 利用 {{ var }} 和 for 遍历标签 将数据写入：

    ```js
    {% for movie in movie_data %}
        <tr>
            <th>{{ movie.id }}</th>
            <td>{{ movie.review }}</td>
            <td>{{ movie.n_star }}</td>
            <td class="text-nowrap">{{  movie.sentiment }}</td>
        </tr>
    {% endfor %}
    ```
