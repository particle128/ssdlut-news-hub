#!/usr/bin/env python
# -*- coding=utf-8 -*-

import requests , re , redis , urllib , logging , time
from BeautifulSoup import BeautifulSoup
from apscheduler.scheduler import Scheduler
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from config import *
from web_server import *

# *** apscheduler使用logging模块，需要初始化一下。默认等级WARNING，因为有些模块requests、apscheduler会以debug或info的等级输出一些信息。而我对这些信息不感兴趣。
logging.basicConfig(filename=LOG_PATH,format='%(asctime)s - %(levelname)s - %(message)s',filemode='w') 

class Crawler():
	def __init__(self):
		self.rs=redis.Redis()

	# 没有过期的项目才被保存
	def save_to_redis(self,name,key,a,date):
		if not self.rs.sismember(name+'_outDate',key):
			if self.rs.hsetnx(name,key,a):
				self.times+=1
				print u' newly adds'
			else:
				print u' already exists'
			self.rs.hsetnx(name+'_date',key,date)
		else:
			print u' out of date'
		
	
	def process_url(self,name,root,url,href_form,date_form,date_loc):
		self.times=0
		# 容错
		try:
			req=requests.get(url,timeout=5)
		except requests.exceptions.RequestException as e:
			logging.error(e)
			return
		# *** 写成req.text出错，因为requests认为该页面是gb2312编码，用这种方式解码成unicode串肯定出错。直接传递原来的字符串(utf-8)，让BeautifulSoup进行解码即可
		soup=BeautifulSoup(req.content) 
		all_a=soup.findAll('a',href=href_form)
		# 如果beautifulSoup没法解析
		if not all_a:
			if date_loc=="after":
				pattern=r'(<a[^>]*href="%s"[^>]*>.*?</a>).*?(%s)'%(href_form.pattern,date_form.pattern)
				d=2
				a=1
			else:
				pattern=r'(%s).*?(<a.*?href="%s".*?</a>)'%(date_form.pattern,href_form.pattern)
				d=1
				a=2
			for match in re.finditer(pattern,req.content,flags=re.S): # *** re.S
				key=re.findall(r'\d+',match.group(a))[0]
				aTag=match.group(a).decode('gb2312').replace(u'href="',u'href="'+unicode(root))
				print u'key=',key,u' name=',name
				self.save_to_redis(name,key.decode('gb2312'),aTag,match.group(d).decode('gb2312'))
		# 如果beautifulSoup可以解析
		else:
			for a in all_a: 
				# href中的数字当作key
				key=re.findall(r'\d+',a['href'])[0]
				a['href']=unicode(root)+a['href']
				# *** 写成a.next出错
				if date_loc=='after':
					date=a.findNext(text=date_form)
				else:
					date=a.findPrevious(text=date_form)
				date=date_form.findall(date)[0]
				print u'key=',key,u' name=',name
				self.save_to_redis(name,key,a,date)
		logging.warning('%d new records added to %s'%(self.times,name))#.decode('utf-8')

	def run(self):
		logging.warning('crawler start...')
		for src in SOURCE:
			self.process_url(src['name'],src['root'],src['url'],src['href_form'],src['date_form'],src['date_loc'])
		logging.warning('crawler end...')

if __name__=='__main__':

	# 等待网络功能正常使用再运行
	time.sleep(60*2)

	crawler=Crawler()
	crawler.run() 

	sched=Scheduler()
	sched.start()
	sched.add_cron_job(crawler.run,hour=INTERVAL['hour'],minute=INTERVAL['min'],second=INTERVAL['sec'])

	# 80端口号需要管理员权限
	httpd=HTTPServer(('127.0.0.1',8080),HttpHandler)
	httpd.serve_forever()



