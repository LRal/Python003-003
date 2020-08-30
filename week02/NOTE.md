# 应对反爬虫

主要关注三个问题：  

- 伪造更真实的 Headers
- 针对不同的验证码采取不同的应对手段
- 使用随机代理 ip

## 更真实的 Headers

> Headers 是用于浏览器向服务器发送的头信息  
> 查看方法：F12 -> Network -> 刷新网页 -> 点击名称列表里的项目 -> Headers，里面有 Headers 各种参数的信息  
> 反爬虫主要关注的参数有 **User-Agent**, **Referer**, **Host**, **Cookies**  
> 可使用 "手动查看 - 在代码中添加" 的方法，将 headers 参数一一填充完整，但是部分参数(如Cookies)具有时效性，导致每次爬虫都要手动获取  
> 本篇笔记将分享自动填入 **User-Agent** 和 **Cookies** 的方法

### 使用随机的 User-Agent

使用随机的 User-Agent，让服务器以为每一次请求都是从不同的客户端发起的，降低被反爬几率

```python
# pip install fake-useragent
from fake-useragent import UserAgent
USER_AGENT = UserAgent(verify_ssl=False).random
```

### 获取 Cookies 的两个方法

> Cookies 不仅仅用于模拟更真实的 Headers，部分网页还有登录后才能查看信息的限制，因此很有必要在爬虫程序中添加 Cookies
> 与 Headers 其他参数不同的是，Cookies 可以以其他方式保存，而不一定写在 Headers 字典中

#### 利用 Session

> 在 requests 库中，通过 Session 对象发出的请求，能够保持相同的 Cookies。  

```python
import requests
session = requests.Session()
response = session.get(url='你的url',headers={'你的headers'})
cookies = session.cookies
```

#### 利用 Selenium 自动登录

> 当遇到那些需要点击操作才能获取的信息时，可以使用 Selenium 库。  
> Selenium 库有专门的方法 .get_cookies() 来获取 Cookies。  

```python
# pip install selenium
from selenium import webdriver

# 需要先配置好对应的 WebDriver （具体查看"环境配置"笔记）
browser = webdirver.Edge()
browser.get('url')
cookies = browser.get_cookies()
```

## 验证码识别

> 验证码的种类多样，解决方法也不一，下面以经典的识别字母验证码为例。  
> 流程：打开图片 - 图片灰度化 - 图片二值化  

```python
# 先安装依赖库libpng, jpeg, libtiff, leptonica
# brew install leptonica
# 安装tesseract
# brew install  tesseract
# 与python对接需要安装的包
# pip3 install Pillow
# pip3 install pytesseract

import requests
import os
from PIL import Image
import pytesseract

# 下载图片
# session = requests.session()
# img_url = 'https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1320441599,4127074888&fm=26&gp=0.jpg'
# agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# headers = {'User-Agent': agent}
# r = session.get(img_url, headers=headers)

# with open('cap.jpg', 'wb') as f:
#     f.write(r.content)

# 打开并显示文件
im = Image.open('cap.jpg')
im.show()

# 灰度图片
gray = im.convert('L')
gray.save('c_gray2.jpg')
im.close()

# 二值化
threshold = 100
table = []

for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

out = gray.point(table, '1')
out.save('c_th.jpg')

th = Image.open('c_th.jpg')
print(pytesseract.image_to_string(th,lang='chi_sim+eng'))

# 各种语言识别库 https://github.com/tesseract-ocr/tessdata
# 放到 /usr/local/Cellar/tesseract/版本/share/tessdata
```

## 使用随机代理 ip

利用 scrapy 中间件使用随机代理 ip。

### 获取随机代理 ip 列表

可到 Github 查看。  
如 https://github.com/clarketm/proxy-list 。  

### 添加自定义中间件

> 位置： <spiders\>/<spiders\>/middlewares.py

```python
# 自定义中间件，能够在爬虫时使用随机 ip
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

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')

        return cls(auth_encoding, http_proxy_list)

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
```

### 添加相应的设置

> 位置： <spiders\>/<spiders\>/settings.py

```python
# 使自定义中间件生效
DOWNLOADER_MIDDLEWARES = {
    'spiders.middlewares.SpidersDownloaderMiddleware': 543,
    'spiders.middlewares.RandomHttpProxyMiddleware': 400,
}

# 把你获取到的随即代理 ip 列表在这里加上
HTTP_PROXY_LIST = [
     'http://186.251.95.155:8080',
     'http://212.83.157.6:5836',
]
```
