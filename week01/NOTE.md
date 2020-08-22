# Scrapy 入门
## 框架架构
![scrapy][scrapy_url]  

## 实现一个最简单的 Scrapy 爬虫
### 1. 安装
```
pip install scrapy
```  

### 2. 创建项目
#### 2.1 创建新项目<spiders>
`scrapy startproject spiders`

#### 2.2 进入包含各组件的 .py 文件的 <spiders> 文件夹
`cd spiders\spiders`

#### 2.3 创建新的 spider 模板
模板包括名称<example>和要爬的域名<example.com>  
`scrapy genspider example example.com`

### 3. 写爬虫函数（以豆瓣 TOP250 为例）
> 爬虫基本思路：  
> 翻页下载子页面 url -> 解析子页面 -> 提取内容 -> 整理内容  
#### 3.1 一些基本参数的设定
##### 3.1.1 设置 name, allowed_domains, start_urls
> 位置： \<spiders\>/\<spiders\>/spiders/\<example\>.py  
```python
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    # name: 你之前定义的爬虫项目模板的名称，不用改
    # allowed_domains: 设置爬虫的域名范围，防止自动爬到了别的网站
    # start_urls: 设置第一次爬的 url，获取头部信息
```

##### 3.1.2 设置 items.py
> 位置： \<spiders\>/\<spiders\>/items.py  
```python
class MoviesItem(scrapy.Item):
    # 按以下格式定义你要爬取的信息标题:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
```

##### 3.1.3 设置 settings.py
> 位置：【】

#### 3.2 翻页下载子页面
##### 3.2.1 写出初次请求 start_requests.()
> 位置： \<spiders\>/\<spiders\>/spiders/example.py  
```python
# 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
# start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
# 引擎再指挥其他组件向网站服务器发送请求，下载网页
def start_requests(self):
   url = [
      f'https://movie.douban.com/top250?start={i*25}' for i in range(0, 10)]
   yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
   # url 请求访问的网址
   # callback 回调函数，引擎回将下载好的页面(response对象)发给该方法，执行数据解析
   # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数
   # dont_filter=False 表示去重
```

##### 3.2.2 写出解析函数 parse()
> 位置： \<spiders\>/\<spiders\>/spiders/example.py  
```python
# 导入 scrapy 针对 xml 的 Selector
from scrapy.selector import Selector
# 导入你之前设置好的 items
from movies.items import MoviesItem

def parse(self, response):
   items = []
   movies = Selector(response=response).xpath('//div[@class="hd"]')
   for movie in movies:
      item = MoviesItem()
      title = movie.xpath('./a/span/text()')
      link = movie.xpath('./a/@href')
      item['title]'] = title
      item['link'] = link
      items.append(item)
```

#### 3.3 解析子页面
【】




[scrapy_url]: https://camo.githubusercontent.com/e0898bedcb0e4d064876c5d4930edc62d6fd0de8/68747470733a2f2f646f63732e7363726170792e6f72672f656e2f6c61746573742f5f696d616765732f7363726170795f6172636869746563747572655f30322e706e67