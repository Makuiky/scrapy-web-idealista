import scrapy


class PruebaSpider(scrapy.Spider):
    name = 'prueba'
    allowed_domains = ['idealista.com']
    start_urls = ['http://idealista.com/']

    def parse(self, response):
        pass
