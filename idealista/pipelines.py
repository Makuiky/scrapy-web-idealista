# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#import pymongo

import sqlite3
from itemadapter import ItemAdapter
from urllib.parse import quote
import re
class SqliteRutinapag(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('idealista.db')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS paginas_pisos
                         (url_pag TEXT UNIQUE)''')
        

    def process_item(self, item, spider):
            self.guardar_pag_pisos(item)
            return item

    def guardar_pag_pisos(self, item):      
        self.cur.execute("""INSERT OR IGNORE INTO paginas_pisos values (?)""",(
            item.get('url'),
        ))
        self.conn.commit()
    def close_spider(self, spider):
        self.cur.close()

class SqliteRutinaurlpiso(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('idealista.db')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS urls_pisos
                         (url_piso TEXT UNIQUE)''')
        

    def process_item(self, item, spider):
            self.guardar_url_pisos(item)
            return item

    def guardar_url_pisos(self, item):  
        if re.search(r'.+/[0-9]',item.get('urlp')):    
            self.cur.execute("""INSERT OR IGNORE INTO urls_pisos values (?)""",(
                item.get('urlp'),
            ))
            self.conn.commit()
    def close_spider(self, spider):
        self.cur.close()