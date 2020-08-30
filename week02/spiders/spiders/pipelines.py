# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql


class SpidersPipeline:
    def open_spider(self, spider):
        self.connection = pymysql.connect(host='localhost',
                                          port=3306,
                                          user='root',
                                          password='12345678',
                                          database='test_db',
                                          charset='utf8')

        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        insert_sql = 'INSERT INTO maoyan(title, genre, release_date) VALUES(%s,%s,%s)'
        movie_info = (item['title'], item['genre'], item['release_date'])

        try:
            self.cursor.execute(insert_sql, movie_info)
            self.connection.commit()
        except Exception:
            self.connection.rollback()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
