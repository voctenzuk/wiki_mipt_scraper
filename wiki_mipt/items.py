# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MiptLecturer(scrapy.Item):
    full_name = scrapy.Field()
    birth_day = scrapy.Field()
    teach_place = scrapy.Field()
    degree = scrapy.Field()
    knowledge = scrapy.Field()
    teaching_skill = scrapy.Field()
    commication_skill = scrapy.Field()
    easy_exam = scrapy.Field()
    overall_score = scrapy.Field()
