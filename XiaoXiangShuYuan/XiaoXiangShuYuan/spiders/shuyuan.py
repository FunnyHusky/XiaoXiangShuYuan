# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from XiaoXiangShuYuan.items import XiaoxiangshuyuanItem,XiaoXiangDetailItem,XiaoxiangslaveItem
from XiaoXiangShuYuan.redisUtil import inserintotc,inserintota
from scrapy_redis.spiders import RedisSpider
import sys

class ShuyuanSpider(scrapy.Spider):
	name = 'shuyuan'
	allowed_domains = ['www.xxsy.net']
	initurl ="http://www.xxsy.net/search?s_wd=&sort=9&pn="
	start_urls=[]
	characterUrl ="http://www.xxsy.net/partview/GetChapterList?bookid=%s&noNeedBuy=0&special=0"
	pageRange =2
	#def __init__(self,start,end):
	#	for x in range(1,self.pageRange):
	#		realUrl =self.initurl+str(x)
	#		self.start_urls.append(realUrl)
	def start_requests(self):
		for x in range(1,self.pageRange):
			realUrl =self.initurl+str(x)
			yield Request(realUrl,callback=self.parse)
	def parse(self, response):
		print("parse url ",response.url)
		selector = Selector(text=response.body.decode("UTF-8"))
		lis = selector.xpath('//div[@class="result-list"]/ul/li').extract()
		print(len(lis))
		for li in lis: #每一本书
			item = XiaoxiangshuyuanItem()
			liSelector = Selector(text=li)
			url = liSelector.xpath('//a[@class="book commonbook"]/@href').extract_first() #http://www.xxsy.net/info/937137.html
			url ="http://www.xxsy.net"+url
			item['url'] =url
			yield Request(url,callback=self.parse_detail)
			image = liSelector.xpath('//img/@data-src').extract_first() #小说图片
			item['image'] =image
			bookName = liSelector.xpath('//div[@class="info"]/h4/a/text()').extract_first() #小说书本名
			item['name'] =bookName
			author = liSelector.xpath('//span[@class="subtitle"]/a[1]/text()').extract_first() #小说作者
			item['author'] =author
			bookTypes = liSelector.xpath('//span[@class="subtitle"]/a[2]/text()').extract_first() #小说类别
			item['booktype'] =bookTypes
			status = liSelector.xpath('//span[@class="subtitle"]/span/text()').extract_first() #小说状态
			item['status'] =status
			bookType = liSelector.xpath('//a[@class="tags"]/text()').extract() #小说标签类型
			tags =""
			for x in bookType:
				tags+=x
				tags+="&&"
			item['type'] =tags
			detail = liSelector.xpath('//p[@class="detail"]/text()').extract_first()
			item['detail'] =detail
			#<p class="number"><span>月点击：7564</span><span>月票：68</span><span>更新：2018-08-03 23:47:55</span><span>字数：1853512</span></p>
			monthClick = liSelector.xpath('//p[@class="number"]/span[1]/text()').extract_first()
			item['monthClick'] =monthClick
			monthTicket = liSelector.xpath('//p[@class="number"]/span[2]/text()').extract_first()
			item['monthTicket'] =monthTicket
			updateTime = liSelector.xpath('//p[@class="number"]/span[3]/text()').extract_first()
			item['updateTime'] =updateTime
			letterCount = liSelector.xpath('//p[@class="number"]/span[4]/text()').extract_first()
			item['letterCount'] =letterCount
			yield item
	def parse_detail(self,response):
		print("parse_detail",response.url)
		selector = Selector(text=response.body.decode("UTF-8"))
		name = selector.xpath('//div[@class="title"]/h1/text()').extract_first()
		author =selector.xpath('//div[@class="title"]/span/a/text()').extract_first()
		author_level = selector.xpath('//div[@class="author-profile"]/a[1]/@title').extract_first()
		custom_image = selector.xpath('//img[@class="avatar"]/@src').extract_first()
		author_description = selector.xpath('//div[@id="authorintro"]/p/text()').extract()
		description_result =""
		for x in author_description:
			description_result+=x
		instruction = selector.xpath('//dl[@class="introcontent"]/dd/p/text()').extract()
		instruction_result = ""
		for x in instruction:
			instruction_result+=x
		scope = selector.xpath('//div[@id="bookstar"]/@data-score').extract_first()
		bigImage =selector.xpath('//dl[@class="bookprofile"]/dt/img/@src').extract_first()
		totalcount =selector.xpath('//p[@class="sub-data"]/span[1]/em/text()').extract_first()
		readtime =selector.xpath('//p[@class="sub-data"]/span[2]/em/text()').extract_first()
		collecttime =selector.xpath('//p[@class="sub-data"]/span[3]/em/text()').extract_first()
		detail = XiaoXiangDetailItem()
		detail['name'] =name
		detail['author'] =author
		detail['author_level'] =author_level
		detail['customIamge'] =custom_image
		detail['author_description'] =description_result
		detail['instruction'] =instruction_result
		detail['scope'] =scope
		detail['bigImage'] =bigImage
		detail['totalcount'] =totalcount
		detail['readtime'] =readtime
		detail['collecttime'] =collecttime
		yield detail
		#print(response.url,"========================================")
		urlid = (response.url.split("http://www.xxsy.net/info/"))[1].split(".html")[0]
		yield Request(self.characterUrl%(urlid),callback=self.parse_character)
	def parse_character(self,response):
		print("parse_character ",response)
		selector = Selector(text = response.body.decode("UTF-8"))
		lis = selector.xpath('//li[not(@class)]/a/@href').extract()
		for x in lis:
			yield Request("http://www.xxsy.net"+x,callback=self.parse_content)
	def parse_content(self,response):
		selector = Selector(text=response.body.decode("UTF-8"))
		characterName = selector.xpath('//h1[@class="chapter-title"]/text()').extract_first()
		bookName = selector.xpath('//p[@class="chapter-subtitle"]/a[1]/text()').extract_first()
		author =selector.xpath('//p[@class="chapter-subtitle"]/a[2]/text()').extract_first()
		booktype =selector.xpath('//p[@class="chapter-subtitle"]/a[3]/text()').extract_first()
		timeandletter =selector.xpath('//p[@class="chapter-subtitle"]/text()').extract()
		letterCount =timeandletter[4]
		updateTime = timeandletter[3]
		content =selector.xpath('//div[@class="chapter-main"]/p/text()').extract()
		contentResult = ""
		for x in content:
			contentResult+=x.strip()
			contentResult+="##"
		slave = XiaoxiangslaveItem()
		slave['characterName'] =characterName
		slave['name'] =bookName
		slave['author'] =author
		slave['booktype'] =booktype
		slave['updateTime'] =updateTime
		slave['letterCount'] =letterCount
		slave['content'] =contentResult
		yield slave