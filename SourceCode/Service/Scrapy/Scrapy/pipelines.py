# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import os
BASE_DIR = '/Users/ds/Code/Python/capstone-project-the-avengers/SourceCode'


class DelishPipeline:
    col = ['title', 'ingredients', 'time', 'steps', 'img_link', 'source', 'link', 'text']

    def __init__(self):
        self.db = sqlite3.connect(os.path.join(BASE_DIR, 'DAO/DataBase/database.db'))
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        item = dict(item)
        try:
            self.insert_item(item)
        except sqlite3.OperationalError:
            self.create_table()
            self.insert_item(item)
        self.db.commit()
        return item

    def create_table(self):
        sql = '''CREATE TABLE ScrapyData(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR NOT NULL,
                    ingredients VARCHAR NOT NULL,
                    time INTEGER,
                    steps VARCHAR,
                    img_link VARCHAR,
                    source VARCHAR,
                    link VARCHAR,
                    text VARCHAR
                    );'''
        self.cur.execute(sql)

    def insert_item(self, item):
        sql = f"INSERT INTO ScrapyData ({', '.join(self.col)}) VALUES " \
              f"('{item['title']}', '{item['ingredients']}', '{item['time']}'," \
              f"""'{item['steps']}', '{item['img_link']}', '{item['source']}', '{item['link']}', "{item['text']}")"""
        self.cur.execute(sql)

    def __del__(self):
        self.db.close()
