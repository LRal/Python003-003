import scrapy
from spiders.items import SpidersItem
from scrapy.selector import Selector

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com/films']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movies_info = Selector(response=response).xpath('//div[@class="movie-hover-info"]')[:10]
        for movie in movies_info:
            movie_info = movie.xpath('./div')
            item = SpidersItem()
            item['title'] = movie_info[0].xpath('./span/text()').get()
            item['genre'] = movie_info[1].xpath('./text()')[1].get().strip()
            item['release_date'] = movie_info[3].xpath('./text()')[1].get().strip()
            yield item