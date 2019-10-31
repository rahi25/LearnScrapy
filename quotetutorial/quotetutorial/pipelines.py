# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Scrape data --> Item Containers --> json /csv files
# Scrape data --> Item Containers --> Pipeline --> SQL/Mongo database

# import sqlite3
import mysql.connector
import pymongo


class QuotetutorialPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()
        self.connect_mongodb()

    def create_connection(self):
        # self.conn = sqlite3.connect("myquotes.db")
        self.conn = mysql.connector.connect(host='localhost', user='root', passwd='Ehsan@1371', database='myquotes')

        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.curr.execute("""create table quotes_tb(
                        quote text,
                        author text,
                        tag text)""")

    # connected to mongodb
    def connect_mongodb(self):
        self.mongo_conn = pymongo.MongoClient('localhost')
        db = self.mongo_conn['myquotes']
        self.collection = db['quotes_tb']

    def process_item(self, item, spider):
        # insert into mongodb
        self.collection.insert(dict(item))

        self.store_db(item)

        print("Pipeline:" + item['quote'][0])
        return item

    def store_db(self, item):
        # ? ==> for sqlite3
        # %s ==> for mysql

        self.curr.execute("""INSERT INTO quotes_tb VALUES (%s,%s,%s)""", (
            item['quote'][0],
            item['author'][0],
            item['tag'][0]
        ))
        self.conn.commit()
