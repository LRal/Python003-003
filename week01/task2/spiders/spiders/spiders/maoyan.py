import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com/films']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movies_info = Selector(response=response).xpath('//div[@class="movie-hover-info"]')[:10]
        for movie_info in movies_info:
            item = SpidersItem()
            item['title'] = movie_info.xpath('./div[1]/span/text()').get()
            item['genre'] = movie_info.xpath('./div[2]/text()')[1].get().strip()
            item['release_date'] = movie_info.xpath('./div[4]/text()')[1].get().strip()
            yield item
