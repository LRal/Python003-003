# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpidersPipeline:
    def process_item(self, item, spider):
        title = item['title']
        genre = item['genre']
        release_date = item['release_date']
        output = f'|{title}|\t|{genre}|\t|{release_date}|\n\n'

        with open('./movie_info.txt', 'a+', encoding='gbk') as article:
            article.write(output)
        return item
