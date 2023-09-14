# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from http.client import PRECONDITION_FAILED
import scrapy


class Piso(scrapy.Item):
    # define the fields for your item here like:
    nombre = scrapy.Field()
    idpiso = scrapy.Field()
    ubicacion = scrapy.Field()
    precio = scrapy.Field()
    eurosporm2 = scrapy.Field()
    m2const = scrapy.Field()
    m2util = scrapy.Field()
    habitaciones = scrapy.Field()
    wc = scrapy.Field()
    planta = scrapy.Field()
    ascensor = scrapy.Field()
    urlpiso =scrapy.Field()
    calle = scrapy.Field()
    barrio = scrapy.Field()
    distrito = scrapy.Field()
    exteinte = scrapy.Field() 
    pass



class UrlPag(scrapy.Item):
    url= scrapy.Field()
    links = scrapy.Field()
    cantpisos = scrapy.Field()
    pass

class UrlPiso(scrapy.Item):
    urlp= scrapy.Field()
    linksp = scrapy.Field()
    pass