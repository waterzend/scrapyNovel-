# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import sys


class YunxizhuanPipeline(object):

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        db_args = dict(
            host='127.0.0.1',
            db='yunxizhuan',
            user='root',
            passwd='root',
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        self.dbpool = adbapi.ConnectionPool("MySQLdb", **db_args)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_into_table, item)
        query.addErrback(self._handle_error, item, spider)
        return item

    def insert_into_table(self, conn, item):
        query = "insert into content(id,title,content) values (%s,%s,%s)"
        arg = (item["id"], item["title"], item["content"])
        conn.execute(query, arg)

    def _handle_error(self, failue, item, spider):
        print(failue)
