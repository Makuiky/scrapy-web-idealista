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
from scrapy.http import Request
import sqlite3
import re

class IdealistaSpider(scrapy.Spider):
    # Nombre de la araña
    name = 'idealista'
    custom_settings = {
        'ITEM_PIPELINES': {'idealista.pipelines.SqliteRutinaItemsPiso': 300,}
    }

    allowed_domains = ['idealista.com']
    
    #start_urls = [
    #    'https://www.idealista.com/inmueble/94595655',
    #    'https://www.idealista.com/inmueble/97795476/'

    #]
    def start_requests(self):
        conn =sqlite3.connect('idealista.db')
        cur=conn.cursor()
        cur.execute('SELECT url_piso FROM urls_pisos')
        rows=cur.fetchall()
        for line in rows:
            yield Request(line[0])
        cur.close()
    

    def parse(self, response):
        piso = Piso()
        piso['nombre'] = response.xpath('//span[@class="main-info__title-main"]/text()').extract_first()
        piso['ubicacion'] = response.xpath('//span[@class="main-info__title-minor"]/text()').extract_first()
        piso['precio'] = int(''.join(re.findall(r'[0-9]+',response.xpath('//strong[@class="flex-feature-details"]/text()').extract_first())))
        piso['eurosporm2'] = int(''.join(re.findall(r'[0-9]+',response.xpath('//p[@class="flex-feature squaredmeterprice"]/span[2]/text()').extract_first())))

        m2= re.findall(r'[0-9]+',response.xpath('//div[@class="details-property_features"]/ul[1]/li[contains(text(),"m²")]/text()').extract_first())
        piso['m2const'] = int(m2[0])
        if len(m2)>1:
            piso['m2util'] = int(m2[1])

        piso['habitaciones'] = int(re.findall(r'[0-9]+',response.xpath('//div[@class="details-property_features"]/ul[1]/li[contains(text(),"habitaciones")]/text()').extract_first())[0])
        piso['wc'] = int(re.findall(r'[0-9]+',response.xpath('//div[@class="details-property_features"]/ul[1]/li[contains(text(),"baño")]/text()').extract_first())[0])

        plantaextint = response.xpath('//div[@class="details-property_features"][2]/ul/li[contains(text(),"Planta")]/text()').extract_first() 
        piso['planta'] = int(re.findall(r'[0-9+]',plantaextint)[0])
        piso['exteinte'] = re.search(r'\b\w+\b$', plantaextint).group()

        piso['ascensor'] = response.xpath('//div[@class="details-property_features"][2]/ul/li[contains(text(),"ascensor")]/text()').extract_first()
        piso['urlpiso'] =response.url
        piso['idpiso'] =int(re.findall(r'[0-9]+',response.url)[0])
        piso['calle'] = response.xpath('//li[@class="header-map-list"][1]/text()').extract_first().strip()
        piso['barrio'] = response.xpath('//li[@class="header-map-list"][2]/text()').extract_first().strip()
        piso['distrito'] = response.xpath('//li[@class="header-map-list"][3]/text()').extract_first().strip()
        
        yield piso
