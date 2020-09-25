# Scrapy 入门

本文表示一个 project 名称为<project\>，spider 模板名称为<spider\>，域名为<spider.com\>，获取信息为<info1\>和<info2\>，用了两层解析函数的例子。

## 框架架构

![scrapy][scrapy_url]  

[scrapy_url]: https://camo.githubusercontent.com/e0898bedcb0e4d064876c5d4930edc62d6fd0de8/68747470733a2f2f646f63732e7363726170792e6f72672f656e2f6c61746573742f5f696d616765732f7363726170795f6172636869746563747572655f30322e706e67

## 安装

`pip install scrapy`

> 成功标志：终端能运行 scrapy 程序

## 创建 project 和 spider

### 创建 project

`scrapy startproject <project>`

### 创建 spider

首先推荐来到 <project\>\\<project\> 文件夹下。

`scrapy genspider <spider> <spider.com>`

#### 运行爬虫命令

`scrapy crawl <spider>`

## 爬虫前配置

### items.py

Scrapy 把爬取得到的信息存放于一个叫 item 对象中。
你需要先设置好，你想要爬取的信息标题。

```python
# <spider>\<spider>\items.py

class <Spiders>Item(scrapy.Item):
    # 按以下格式定义你要爬取的信息标题:
    # name = scrapy.Field()
    <info1> = scrapy.Field()
    <info2> = scrapy.Field()
```

### pipelines.py

让你爬取的数据，通过不同的管道，保存在不同的媒介中。

#### 管道的编写

##### MySQL

写一个负责将爬虫数据存放在 MySQL 中的类，这种类就是在 Scrapy 中的管道。

```python
# <spider>\<spider>\pipelines.py
import pymysql  # 使用 pymysql 在 python 中对 MySQL 进行操作。

class MySQLPipeline:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            pwd=crawler.settings.get('MYSQL_PWD'),
            db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.connection = pymysql.connect(
            self.host, self.user, self.pwd, self.db
        )

    def process_item(self, item, spider):
        sql = 'INSERT INTO tennet(review, star_rating, comment_time) VALUES(%s, %s, %s)'
        value = (item['review'], item['star_rating'], item['comment_time'])

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, value)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
        finally:
            self.cursor.close()

        return item

    def close_spider(self, spider):
        self.connection.close()
```

> **from_crawler()**：负责从 settings.py 中获取自定义设置。
> 比如在这个例子中，获取 MYSQL_HOST 等这些自己加上去的设置项。
> **open_spider()**、**close_spider()**：这两个函数分别会在管道启动、关闭时各执行一次。
> 利用这个特性，这两个函数一般用来实现一些类似启动关闭之类的功能。
> **process_item()**：是管道中的核心函数，接收保存了爬虫数据的 item 参数，并对这些数据进行处理。
> 这四个函数都是 Scrapy 中的专有函数，**不能随意改名**。

##### CSV

写一个负责将爬虫数据存放在 CSV 文件中的类。
可以用来测试爬到的数据是否符合预期，要是不符合的话想删就删。
数据库就没有这么方便。

```python
# <spider>\<spider>\pipelines.py
class CSVPipeline:
   def process_item(self, item, spider):
      <info1> = item['<info1>']
      <info2> = item['<info2>']

      output = f'|{<info1>}| |{<info2>}|\n'
      with open('./info.txt', 'a', encoding='gbk') as article:
         article.write(output)
      return item
```

#### 启用 ITEM_PIPELINES 组件

编写好管道后，我们还要进行相关的设置，设置这些组件是否运行以及运行的顺序。

```python
# <spider>\<spider>\settings.py
# 启用 Item Pipeline 组件，数字范围 0-1000，数值越低，组件的优先级越高

ITEM_PIPELINES = {
    '<project>.pipelines.MySQLPipeline': 300,
    '<project>.pipelines.CSVPipeline': 300,
}
```

> 启用 组件/中间件 规则：
> 值设为 None 时，不启用
> 值设为数字，范围 0-1000，数值越低，组件的优先级越高

### 反爬虫

#### USER_AGENT

设置一个随机的假 USER_AGENT，模拟真实的浏览器。

```python
# pip install fake-useragent
# <spider>\<spider>\settings.py

from fake-useragent import UserAgent
USER_AGENT = UserAgent(verify_ssl=False).random
```

#### Cookies

#### 并发设置

Scrapy 基于 Twisted 异步框架，能够设置并发相关的参数。
通过设置并发相关的参数，调整延迟，降低服务器对 IP 进行反爬的几率。

```python
# <spider>\<spider>\settings.py

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 并发请求最大值
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# 设置爬虫延迟，降低被反爬的几率
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
# 对单个 域名/IP 进行并发请求的最大值，只能二选一
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
```

#### 随机代理 IP

利用 Scrapy 中间件使用随机代理 IP。

##### 获取随机代理 ip 列表

首先你要有可用的代理 IP 列表。
可以选择购买专业的代理 IP，
也可以选择寻找万人骑的不稳定的免费 IP，如 Github 上的[这个项目](https://github.com/clarketm/proxy-list)。

##### 添加自定义中间件

```python
# <spider>\<spider>\middlewares.py
# 通过继承 Scrapy 内置的 HttpProxyMiddleware，我们写一个可以使用随机代理 IP 的中间件。

import random
from collections import defaultdict
from urllib.parse import urlparse
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured

class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, auth_encoding='utf-8', proxy_list = None):
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
        # 这个 auth_encoding 继承 HttpProxyMiddleware 中原有的代码，我们保留下来。
        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')

        return cls(auth_encoding, http_proxy_list)

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
```

##### 启用中间件

编写好自定义中间件后，我们还要进行相关的设置，设置这些组件是否运行以及运行的顺序。

```python
# 使自定义中间件生效
DOWNLOADER_MIDDLEWARES = {
    '<project>.middlewares.RandomHttpProxyMiddleware': 400,
    '<project>.middlewares.SpidersDownloaderMiddleware': 543,
}

# 把你获取到的随即代理 ip 列表在这里加上
HTTP_PROXY_LIST = [
    'http://199.19.107.10:80',
]
```

## 开始爬虫

Scrapy 中处理爬虫的核心文件是 `<project>\<project>\spiders\<spider>.py`。

### <spider\>.py 解析

这个文件由一个个类组成，每个类对应各自的 spider，习惯上命名为 <spider\>Spider。
每个类的最终目标是返回一个字典类型的 item，这将会通过层层解析函数来实现。
比如第零层函数获取 URL，第一层函数获取电影名，第二层函数获取评分等等。

#### 解析函数前面的三个变量

name, allowed_domains, start_urls

```python
import scrapy

class <spider>Spider(scrapy.Spider):
    name = '<spider>'
    # 你之前定义的爬虫项目模板的名称，crawl 命令后面跟这个名字，不用改

    allowed_domains = ['<spider>.com']
    # 设置爬虫的域名范围，防止自动爬到了别的网站

    start_urls = ['<spider>.com']
    # 设置第一次爬的 url，一般用于登录或获取头部信息
```

#### 第零层解析函数

**start_requests()**，也称初次请求函数，它的名称时固定的。
爬虫启动时，引擎自动调用该方法，并且只会被调用一次，通常用于获取初始 url。

```python
def start_requests(self):
   url = '<spider.com>'
   # 写出初始 url 或 url 列表
   # 这个 url 可以是你手动写好，也可以是直接爬取获得的。

   yield scrapy.Request(url=url, callback=self.parse)
   # callback 负责将写好的 url 发给下一层解析函数 parse
```

#### 第一层解析函数

parse()，官方默认名称，可以更改。

```python
from <project>.items import <project>Item  # 导入你之前设置好的 <project>Item 类
from scrapy.selector import Selector  # 推荐使用 Scrapy 自带的 Selector 进行 XPath 解析
# 当然你也可以选择用其他工具比如 bs4 解析

# 假设第一层解析函数用于获取下一层要解析的 url 和 info1，后面的解析函数依次类推
def parse(self, response):
   item = <project>Item()  # 创建 item 对象

   <info1> = fake_code_to_get_<info1>
   # 你通过各种手段解析网页得到了 <info1>，假设它是第二层解析函数要用到的 url

   item['<info1>'] = <info1>  # 将 <info1> 保存进 item

   yield scrapy.Request(url=<info1>, meta={'item': item}, callback=self.parse2)
```

#### 最后一层解析函数

parse2()，第二层解析函数，名称可以更改。
假设这里是最后一层解析函数。

```python
from scrapy.selector import Selector  # 日常推荐使用 Scrapy 自带的 Selector

def parse2(self, response):

    # 前面的解析函数已经创建 item 对象了，这里就不用再创建了

    <info2> = fake_code_to_get_<info2>
    # 你通过各种手段解析网页得到了 <info2>

    item['<info_2>'] = <info_2>  # 将 <info_2> 保存进 item

    yield item
    # 最后一层解析函数直接返回 item 即可
```

### Scrapy 自带的 Selector

XPath 底层是 C 语言，BeautifulSoup 底层是 Python。
所以，xpath 用得好效率能比 BeautifulSoup 快九条街。
所以，推荐使用 Scrapy 自带的 Selector，它用于 xml 化 html 网页，以便进一步使用 XPath 进行解析。

#### 用法

用法其实非常简单，你只需要记住：

`Selector(response).xpath('XPath').get()`

```python
from scrapy.selector import Selector

response = response_you_get
Selector(response=response).xpath('XPath')  # 解析例子
Selector(response=response).xpath('xpath1').xpath('xpath2')  # 支持将 XPath 分开解析（用于有重复 XPath 时）
Selector(response=response).xpath('XPath').get()  # 返回第一个值（你真正想要的信息）
Selector(response=response).xpath('XPath').getall()  # 列表形式返回所有值（你真正想要的信息）
```

> [Selector 官方文档](https://docs.scrapy.org/en/latest/topics/selectors.html)
> [XPath 教程](https://www.w3school.com.cn/xpath/xpath_syntax.asp)

#### 实例

```python
    def parse(self, response):
        movies_info = Selector(response=response).xpath('//div[@class="movie-hover-info"]')[:10]
        for movie_info in movies_info:
            item = SpidersItem()
            # 血的教训：第二段 XPath 一定不要把开头的点 (.) 给漏了
            item['title'] = movie_info.xpath('./div[1]/span/text()').get()
            item['genre'] = movie_info.xpath('./div[2]/text()')[1].get().strip()
            item['release_date'] = movie_info.xpath('./div[4]/text()')[1].get().strip()
            yield item
```

## 调试

在你想要调试的地方添加两行代码即可。

```python
from scrapy.shell import inspect_response

some_fake_code_here
# 你想从这个位置开始调试
inspect_response(response, self)
# 当 cmd 开始执行 'scrapy crawl <spider>'，运行到这里的时候，终端会变成 scrapy shell，然后你可以开始调试，比如测试写的 XPath 对不对

some_fake_code_here
```

## 分布式爬虫
