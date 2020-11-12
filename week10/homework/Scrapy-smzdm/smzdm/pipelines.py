# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from snownlp import SnowNLP


class MySQLPipeline:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.connection = None
        self.cursor = None

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
        name = item['name']
        date = item['date']
        comment = item['comment']
        stmscore = SnowNLP(item['comment']).sentiments
        value = (name, date, comment, stmscore)
        sql = 'INSERT INTO smartphones(name, date, comment, stmscore) \
            VALUES(%s, %s, %s, %s)'
        self.insert_value(sql, value)
        return item

    def close_spider(self, spider):
        self.connection.close()

    def insert_value(self, sql, value):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, value)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
        finally:
            self.cursor.close()


class CSVPipeline:
    def process_item(self, item, spider):
        name = item['name']
        comment = item['comment']

        output = f'|{name}| |{comment}|\n'
        with open('./info.txt', 'a', encoding='gbk') as article:
            article.write(output)
        return item
