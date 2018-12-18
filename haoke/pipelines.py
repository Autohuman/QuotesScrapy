# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import mysql.connector

class TextPipeline(object):

    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')

class MysqlPipeline(object):
    def __init__(self):   #创建数据库游标（连接）
        self.host = 'localhost'
        self.username = 'root'
        self.password = ''
        self.port = '3306'
        self.database = 'python'

    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(host=self.host, user=self.username, password=self.password, port=self.port, database=self.database)
            self.cursor = self.conn.cursor()
        except:
            print("Conn Error")

    def process_item(self, item, spider):   #插入数据到mysql
        inser = "INSERT INTO quotes (text, author, tags) VALUES(%s, %s, %s)"
        one = (item['text'], item['author'], item['tags'])
        self.cursor.execute(inser, one)
        self.conn.commit()
        return item

    def close(self):
        self.conn.close()

    # def query_formatrs(self, sql_str):  #查询数据，返回列表，每行一个字典，带字段名
    #     try:
    #         self.cursor.execute(sql_str)
    #         rows = self.cursor.fetchall()
    #         r = []
    #         for row in rows:
    #             r.append(dict(zip(self.cursor.column_names, row)))
    #         return r
    #     except:
    #         return False

    # def insert(self):  #插入数据
    #     obj = ()
    #     self.sql_str = "INSERT INTO "
    #     try:
    #         self.cursor.execute(sql_str)
    #         pass
    #     except:
    #         pass










# class MysqlPipeline(object):
#
#     def __init__(self, host, user, db, pwd):
#         self.host = host
#         self.user = user
#         self.db = db
#         self.pwd = pwd
#
#     def open_spider(self, crawler, spider):
#         self.conn = mysql.connector.connect(
#             host=crawler.settings.get('MYSQL_HOST'),
#             user=crawler.settings.get('MYSQL_USER'),
#             db=crawler.settings.get('MYSQL_DB'),
#             pwd=crawler.settings.get('MYSQL_PWD')
#         )
#         return self.conn.cursor()
#
#     def process_item(self, item, spider):
