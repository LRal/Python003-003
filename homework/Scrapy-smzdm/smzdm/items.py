import scrapy

class SmzdmItem(scrapy.Item):
    name = scrapy.Field()
    comment = scrapy.Field()
    date = scrapy.Field()
