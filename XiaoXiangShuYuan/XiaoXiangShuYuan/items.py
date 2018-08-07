# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoxiangshuyuanItem(scrapy.Item):
	url = scrapy.Field()
	status =scrapy.Field()
	image =scrapy.Field()
	type =scrapy.Field()
	monthClick =scrapy.Field()
	detail =scrapy.Field()
	booktype =scrapy.Field()
	monthTicket =scrapy.Field()
	letterCount =scrapy.Field()
	author =scrapy.Field()
	updateTime =scrapy.Field()
	name =scrapy.Field()
	
class XiaoXiangDetailItem(scrapy.Item):
	name = scrapy.Field()
	author = scrapy.Field()
	author_level = scrapy.Field()
	customIamge = scrapy.Field()
	author_description = scrapy.Field()
	instruction = scrapy.Field()
	scope = scrapy.Field()
	bigImage = scrapy.Field()
	totalcount = scrapy.Field()
	readtime = scrapy.Field()
	collecttime = scrapy.Field()
	
class XiaoxiangslaveItem(scrapy.Item):
	characterName =scrapy.Field()
	name =scrapy.Field()
	author =scrapy.Field()
	booktype =scrapy.Field()
	updateTime =scrapy.Field()
	letterCount =scrapy.Field()
	content =scrapy.Field()
