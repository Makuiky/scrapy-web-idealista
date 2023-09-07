# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:07:11 2022

@author: Pablo
"""
from ast import Yield
from itertools import product
from queue import Empty
import scrapy
import csv
from scrapy.linkextractors import LinkExtractor
from idealista.items import Piso
from idealista.items import UrlPiso
from scrapy.http import Request
import sqlite3

class Idealistaurlpiso(scrapy.Spider):
    # Nombre de la araña
    name = 'urlpiso'
    custom_settings = {
        'ITEM_PIPELINES': {'idealista.pipelines.SqliteRutinaurlpiso': 300,}
    }
    allowed_domains = ['idealista.com']
    
    #start_urls = [
        #'https://www.idealista.com/venta-viviendas/valencia-valencia/',
        #'https://www.idealista.com/venta-viviendas/valencia-valencia/pagina-2.htm'
    #]
    def start_requests(self):
        conn =sqlite3.connect('idealista.db')
        cur=conn.cursor()
        cur.execute('SELECT url_pag FROM paginas_pisos')
        rows=cur.fetchall()
        for line in rows:
            yield Request(line[0])
        cur.close()

    def parse(self, response):
        urls = UrlPiso()

        links = LinkExtractor(
            allow_domains=['idealista.com'],
            restrict_xpaths=['//div[@class= "item-info-container"]/a']
            #allow="/es/"
        ).extract_links(response)
        
        outlinks = [] 
        for link in links:
            url = link.url
            outlinks.append(url) # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse) # Generamos la petición

        urls['urlp'] =response.url
        yield urls