# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from data.settings import MYSQL


class a39netDataPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            password=MYSQL['password'],
            database=MYSQL['database']
        )

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            sql = sql = "INSERT INTO a39net(`name`, `introduction`, `altname`, `pathogenic_site`, `department`," \
                        " `population`, `symptom`, `inspect`, `complication`, `treatment`, `medication`, `cause`) VALUES (%s, %s, %s, %s, %s," \
                        " %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (item['name'], item['introduction'], item['altname'], item['pathogenic_site'],
                                 item['department'], item['population'], item['symptom'], item['inspect'],
                                 item['complication'], item['treatment'], item['medication'], item['cause']))
            print('A39net-insert')
            self.conn.commit()
        except:
            print('a39net写入异常')
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item
