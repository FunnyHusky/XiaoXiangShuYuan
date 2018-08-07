# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from XiaoXiangShuYuan.items import XiaoxiangshuyuanItem,XiaoXiangDetailItem,XiaoxiangslaveItem
import redis
class XiaoxiangshuyuanPipeline(object):
	@classmethod
	def from_crawler(cls,crawler):
		settings = crawler.settings
		host = settings['MYSQL_HOST']
		port = settings['MYSQL_PORT']
		user = settings['MYSQL_USER']
		pwd = settings['MYSQL_PASSWORD']
		db = settings['MYSQL_DATABASE']
		return cls(host,port,user,pwd,db)
	def __init__(self,host,port,user,pwd,db):
		self.host = host
		self.port = port
		self.user = user
		self.pwd = pwd
		self.db = db
	def process_item(self, item, spider):
		pymysql.install_as_MySQLdb()
		conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.pwd,db=self.db,charset='utf8')
		cursor = conn.cursor()
		if isinstance(item,XiaoxiangshuyuanItem):
			sql ="insert into book (status,image,type,monthClick,detail,booktype,monthTicket,letterCount,startUrl,author,updateTime,name)\
			values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
			sql = sql%(item['status'],item['image'],item['type'],item['monthClick'],item['detail'],item['booktype'],item['monthTicket'],item['letterCount'],item['url'],item['author'],item['updateTime'],item['name'])
			cursor.execute(sql)
			conn.commit()
			cursor.close()
			conn.close()
			return item
		if isinstance(item,XiaoXiangDetailItem):
			print("detail item *****************************************************************")
			sql ="insert into info(name,author,author_level,customIamge,author_description,instruction,scope,bigImage,totalcount,readtime,collecttime) \
			values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
			sql =sql%(item['name'],item['author'],item['author_level'],item['customIamge'],item['author_description'],item['instruction'],item['scope'],item['bigImage'],item['totalcount'],item['readtime'],item['collecttime'])
			cursor.execute(sql)
			conn.commit()
			cursor.close()
			conn.close()
			return item
		if isinstance(item,XiaoxiangslaveItem):
			sql ="insert into content(characterName,name,author,booktype,updateTime,letterCount,content) \
			values('%s','%s','%s','%s','%s','%s','%s')"
			sql =sql%(item['characterName'],item['name'],item['author'],item['booktype'],item['updateTime'],item['letterCount'],item['content'])
			cursor.execute(sql)
			conn.commit()
			cursor.close()
			conn.close()
			return item
		
