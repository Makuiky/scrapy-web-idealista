import subprocess
scrapy_command = 'scrapy crawl idealista'

spiders=['scrapy crawl urlpag','scrapy crawl urlpiso','scrapy crawl idealista']

for spider in spiders:
    subprocess.run(spider, shell=True, check=True)