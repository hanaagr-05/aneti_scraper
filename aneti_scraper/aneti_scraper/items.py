# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AnetiScraperItem(scrapy.Item):
    reference = scrapy.Field()
    profession = scrapy.Field()
    activite = scrapy.Field()
    region = scrapy.Field()
    nb_poste = scrapy.Field()
    date_post = scrapy.Field()
    status = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
