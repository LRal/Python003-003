# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql


class SpidersPipeline:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

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
        sql = 'INSERT INTO maoyan(title, genre, release_date) VALUES(%s, %s, %s)'
        value = (item['title'], item['genre'], item['release_date'])

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, value)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
        finally:
            self.cursor.close()

        return item

    def close_spider(self, spider):
        self.connection.close()
