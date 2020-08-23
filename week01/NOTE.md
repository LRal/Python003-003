# Scrapy 入门
## 框架架构
![scrapy][scrapy_url]  

## 实现一个 Scrapy 爬虫
> 以下代码表示一个 project 名称为<spiders\>，spider 模板名称为<example\>，域名为<example.com\>，获取信息<info_1\>和<info_2\>，用了两层解析函数的例子
### 1. 安装 Scrapy
```
pip install scrapy
```  

### 2. 创建项目
#### 2.1 创建新项目<spiders>
`scrapy startproject <spiders>`

#### 2.2 进入包含各组件的 .py 文件的 <spiders> 文件夹
`cd <spiders>\<spiders>`

#### 2.3 创建新的 spider 模板
模板包括名称<example>和要爬的域名<example.com>  
`scrapy genspider <example> <example.com>`

### 3. 写爬虫函数 
#### 3.1 一些基本参数的设定
##### 3.1.1 设置 name, allowed_domains, start_urls
> 位置： <spiders\>/<spiders\>/spiders/<example\>.py  
```python
class <Example>Spider(scrapy.Spider):
    name = '<example>'
    allowed_domains = ['<example>.com']
    start_urls = ['<example>.com']
    # name: 你之前定义的爬虫项目模板的名称，不用改
    # allowed_domains: 设置爬虫的域名范围，防止自动爬到了别的网站
    # start_urls: 设置第一次爬的 url，获取头部信息
```

##### 3.1.2 设置 items.py
> 位置： <spiders\>/<spiders\>/items.py  
```python
class <Spiders>Item(scrapy.Item):
    # 按以下格式定义你要爬取的信息标题:
    # name = scrapy.Field()
    <info_1> = scrapy.Field()
    <info_2> = scrapy.Field()
```

##### 3.1.3 设置 settings.py
> 位置：<spiders\>/<spiders\>/settings.py  
```python
# 在 settings.py 中有一些必要的代码行默认被注释，只要把注释号去掉就行
# Scrapy 会在初次请求自动获得 USER_AGENT
USER_AGENT = '<spiders> (+http://www.yourdomain.com)'
# 设置下载间隔（默认为3）
DOWNLOAD_DELAY = 3
# 启用 Item Pipeline 组件，数字范围 0-1000，数值越低，组件的优先级越高
ITEM_PIPELINES = {
    'spiders.pipelines.SpidersPipeline': 300,
}
```

#### 3.2 开始爬虫
> 位置： \<spiders\>/\<spiders\>/spiders/<example>.py  
> 各层解析的最终目标是返回一个字典类型的 item
##### 3.2.1 初次请求（第零层）函数 start_requests()
```python
# start_requests() 的名称是固定的
# 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于获取初始 url。
def start_requests(self):
   url = '<example.com>'
   # 写出初始 url 或 url 列表

   yield scrapy.Request(url=url, callback=self.parse)
   # callback 负责将写好的 url 发给下一层解析函数
   # 这里可以使用callback指定新的函数，而非默认的 parse
```

##### 3.2.2 第一层解析函数 parse() 
```python
# 导入你之前设置好的 <Spiders>Item
from <spiders>.items import <Spiders>Item

# 当你选择用 Xpath 解析时，导入 scrapy 的 Selector
# Selector 用法举例：
# <info_1> = Selector(response=response).xpath('your_xpath')
from scrapy.selector import Selector

# 第一层解析函数用于获取下一层要解析的 url 和 item 的部分 info，后面的解析函数依次类推
def parse(self, response):
   item = <Spiders>Item()
   # 创建空 item

   <info_1> = fake_code_to_get_<info_1>
   # 使用 BeautifulSoup 或 Xpath 解析，假设这里得到了 <info_1>，假设它是第二层解析函数要用到的 url

   item['<info_1>'] = <info_1>
   # 将 <info_1> 保存进 item
   yield scrapy.Request(url=<info_1>, meta={'item': item}, callback=self.parse2)
```

##### 3.2.3 第二层解析函数 parse2()
```python
def parse2(self, response):
   <info_2> = fake_code_to_get_<info_2>
   # 使用 BeautifulSoup 或 Xpath 解析，假设这里得到了 <info_2>

   item['<info_2>'] = <info_2>
   # 将 <info_2> 保存进 item
   yield item
```

#### 3.3 保存内容
> 位置： \<spiders\>/\<spiders\>/pipelines.py
```python
class SpidersPipeline:
   def process_item(self, item, spider):
      # item 信息
      <info_1> = item['info_1']
      <info_2> = item['info_2']

      # 保存方式（以 with 语句为例）
      output = f'|{<info_1>}|\t|{<info_2>}|\n'
      with open('./info.txt', 'a+', encoding='gbk') as article:
         article.write(output)
      return item
```  

### 4. 运行项目
> 位置： <spiders\>  
`scrapy crawl <example>`

---
[scrapy_url]: https://camo.githubusercontent.com/e0898bedcb0e4d064876c5d4930edc62d6fd0de8/68747470733a2f2f646f63732e7363726170792e6f72672f656e2f6c61746573742f5f696d616765732f7363726170795f6172636869746563747572655f30322e706e67