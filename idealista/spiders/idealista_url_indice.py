from ast import Yield
from itertools import product
from queue import Empty
import scrapy
import csv
from scrapy.linkextractors import LinkExtractor
from idealista.items import UrlPag
from scrapy.http import Request



class Idealistaurlpag(scrapy.Spider):
    # Nombre de la araña
    name = 'urlpag'
    custom_settings = {
        'ITEM_PIPELINES': {'idealista.pipelines.SqliteRutinapag': 300,}
    }
    allowed_domains = ['idealista.com']
    
    start_urls = [
       
        'https://www.idealista.com/venta-viviendas/valencia/extramurs/',
        'https://www.idealista.com/venta-viviendas/valencia/quatre-carreres/',
        'https://www.idealista.com/venta-viviendas/valencia/poblats-maritims/',
        'https://www.idealista.com/venta-viviendas/valencia/benicalap/',
        'https://www.idealista.com/venta-viviendas/valencia/camins-al-grau/',
        'https://www.idealista.com/venta-viviendas/valencia/rascanya/',
        'https://www.idealista.com/venta-viviendas/valencia/jesus/',
        'https://www.idealista.com/venta-viviendas/valencia/l-olivereta/'
    ]

    def parse(self, response):
        urls = UrlPag()
        
        urls['url'] = response.url
        urls['cantpisos'] = response.xpath('//li[5]/span[@class="breadcrumb-navigation-element-info"]/text()').extract_first()
        yield urls
