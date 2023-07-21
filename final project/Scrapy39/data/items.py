# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class a39Item(scrapy.Item):
    name = scrapy.Field()
    introduction = scrapy.Field()
    altname = scrapy.Field()
    pathogenic_site = scrapy.Field()
    department = scrapy.Field()
    population = scrapy.Field()
    symptom = scrapy.Field()
    inspect = scrapy.Field()
    complication = scrapy.Field()
    treatment = scrapy.Field()
    medication = scrapy.Field()
    cause = scrapy.Field()
    pass

