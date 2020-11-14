"""
爬取 smzdm.com 页面信息
"""

import scrapy
from scrapy.selector import Selector
from smzdm.items import SmzdmItem


class SmartphoneSpider(scrapy.Spider):
    """
    爬取智能手机前十产品的 name, date 和 comment
    """

    name = 'smartphone'
    allowed_domains = ['smzdm.com']
    start_urls = [
        'https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/',
    ]
    product_num = 10  # 爬取产品数
    max_comment_page_num = 1000  # 爬取评论页数

    def parse(self, response):
        """
        爬取产品名称和产品 url
        """

        product_list = Selector(response=response).xpath(
            "//div[@class='z-feed-content ']/h5/a"
        )[:self.product_num]

        for product in product_list:
            item = SmzdmItem()
            item['name'] = product.xpath('./text()').get()
            product_url = product.xpath('./@href').get()
            yield scrapy.Request(
                url=product_url,
                meta={'item': item},
                callback=self.parse_page_url
            )

    def parse_page_url(self, response):
        """
        当产品评论数量为 0 时, 页面没有跳转页码的链接
        因此先通过评论总数, 计算评论总页数, 以获取评论 url
        """
        item = response.meta['item']
        comment_num = Selector(response=response).xpath(
            "//em[@class='commentNum']/text()"
        ).get()
        comment_page_num = int(comment_num) // 30 + 1  # 网页评论数上限 30 条

        for page in range(1, comment_page_num + 1):
            if page > self.max_comment_page_num:
                break
            comment_url = response.url + f'p{page}'
            yield scrapy.Request(
                url=comment_url,
                meta={'item': item},
                callback=self.parse_comments,
                dont_filter=True
            )

    @staticmethod
    def parse_comments(response):
        """
        爬取评论时间和内容
        """

        item = response.meta['item']
        date_list = Selector(response=response).xpath(
            "//div[@id='commentTabBlockNew']//meta/@content"
        ).getall()
        comment_list = Selector(response=response).xpath(
            "//div[@id='commentTabBlockNew']//div[@class='comment_conBox']"
            "/div[last()]//span[@itemprop='description']"
        )

        for date, comment in zip(date_list, comment_list):
            item['date'] = date
            item['comment'] = comment.xpath('string(.)').get()
            yield item
