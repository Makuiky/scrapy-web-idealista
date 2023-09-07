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

        links = LinkExtractor(
            allow_domains=['idealista.com'],
            restrict_xpaths=['//a[@class= "icon-arrow-right-after"]']
            #allow="/es/"
        ).extract_links(response)
        
        outlinks = [] 
        for link in links:
            url = link.url
            outlinks.append(url) # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse) # Generamos la petición

        urls['url'] =response.url
        yield urls
