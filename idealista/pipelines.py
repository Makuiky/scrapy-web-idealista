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
        self.eliminate_table()
        self.create_table()
        
    def create_connection(self):
        self.conn = sqlite3.connect('idealista.db')
        self.cur = self.conn.cursor()

    def eliminate_table(self):
        self.cur.execute('''DROP TABLE paginas_pisos''')                
                        
    def create_table(self):
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS paginas_pisos
                         (url_pag TEXT UNIQUE)''')
        

    def process_item(self, item, spider):
            self.guardar_pag_pisos(item)
            return item

    def guardar_pag_pisos(self, item):
        ultpag= (int(item.get('cantpisos'))//30)+2
        for i in range(1,ultpag):
            urlgenerada = item.get('url')+'pagina-'+str(i)+'.htm'
            self.cur.execute("""INSERT OR IGNORE INTO paginas_pisos values (?)""",(
            urlgenerada,
            ))
        self.cur.execute("""INSERT OR IGNORE INTO paginas_pisos values (?)""",(
            item.get('url'),
            ))
        self.conn.commit()
    def close_spider(self, spider):
        self.cur.close()

class SqliteRutinaurlpiso(object):

    def __init__(self):
        self.create_connection()
        self.eliminate_table()
        self.create_table()
        
    def create_connection(self):
        self.conn = sqlite3.connect('idealista.db')
        self.cur = self.conn.cursor()
        
    def eliminate_table(self):
        self.cur.execute('''DROP TABLE IF EXISTS urls_pisos''')

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

class SqliteRutinaItemsPiso(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('idealista.db')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS items_pisos
                         (id_piso INT PRIMARY KEY, 
                         nombre_piso VARCHAR(200),
                         ubicacion VARCHAR(50),                   
                         precio INT,
                         euros_m2 INT,
                         m2_construido SMALLINT,
                         m2_util SMALLINT,
                         num_habitaciones TINYINT,
                         aseos TINYINT,
                         planta TINYINTUNSIGNED,
                         ascensor VARCHAR(15),
                         url VARCHAR(400),
                         calle VARCHAR(100),
                         barrio VARCHAR(100),
                         distrito VARCHAR(100),
                         disposicion_a_la_calle VARCHAR(10),
                         fecha_de_registro TIMESTAMP
                        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS evolucion_precio_pisos
                        (id_piso INT,
                        precio INT,
                        fecha_de_registro TIMESTAMP   
                        )''')
    def process_item(self, item, spider):
            self.actualizar_precio_piso(item)
            self.guardar_item_piso(item)
            self.registrar_evolucion_piso(item)
            return item
    
    def registrar_evolucion_piso(self,item):
         self.cur.execute('''INSERT INTO evolucion_precio_pisos(
                          id_piso,
                          precio,
                          fecha_de_registro
                          ) VALUES (?,?,CURRENT_TIMESTAMP)''',(
                               item.get('idpiso'),
                               item.get('precio'),
                          ))
    
    def actualizar_precio_piso(self,item):
         self.cur.execute('''UPDATE items_pisos SET precio=?,euros_m2=?, fecha_de_registro=CURRENT_TIMESTAMP WHERE id_piso=?''',(
              item.get('precio'),
              item.get('eurosporm2'),
              item.get('idpiso'),
         ))
    
    def guardar_item_piso(self, item):      
        self.cur.execute("""INSERT OR IGNORE INTO items_pisos(
                         id_piso, 
                         nombre_piso,
                         ubicacion,                   
                         precio,
                         euros_m2,
                         m2_construido,
                         m2_util,
                         num_habitaciones,
                         aseos,
                         planta,
                         ascensor,
                         url,
                         calle,
                         barrio,
                         distrito,
                         disposicion_a_la_calle,
                         fecha_de_registro
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)""",(
                            item.get('idpiso'),
                            item.get('nombre'),
                            item.get('ubicacion'),
                            item.get('precio'),
                            item.get('eurosporm2'),
                            item.get('m2const'),
                            item.get('m2util'),
                            item.get('habitaciones'),
                            item.get('wc'),
                            item.get('planta'),
                            item.get('ascensor'),
                            item.get('urlpiso'),
                            item.get('calle'),
                            item.get('barrio'),
                            item.get('distrito'),
                            item.get('exteinte'),
        ))
        self.conn.commit()
    def close_spider(self, spider):
        self.cur.close()