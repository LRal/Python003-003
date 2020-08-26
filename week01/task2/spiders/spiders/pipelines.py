# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpidersPipeline:
    def open_spider(self, spider):
        print('start spider')

    def process_item(self, item, spider):
        title = item['title']
        genre = item['genre']
        release_date = item['release_date']
        output = f'|{title}| |{genre}| |{release_date}|\n'

        with open('./movie_info.csv', 'a', encoding='gbk') as article:
            article.write(output)
        return item

    def close_spider(self, spider):
        print('close spider')
