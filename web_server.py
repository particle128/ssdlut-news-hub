# -*- coding=utf-8 -*-

import  re , redis , urllib , logging
from urlparse import urlparse, parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from config import *

def generate_page(rs):
	body=''
	for source in SOURCE:
		name=source['name'] 
		items=rs.hgetall(name).items()
		# 显示结果按照新闻id降序排列
		link_list=''
		# 以整数方式比较!!!
		for key,val in sorted(items,reverse=True,key=lambda x: int(x[0])): 
			link_list+='<tr><td>%s</td><td align="center">%s</td><td><a href="http://127.0.0.1:8080?key=%s&name=%s">已阅</a></td></tr>'%(val,rs.hget(name+'_date',key),key,urllib.quote(name))
		link_outAll='<a href="http://127.0.0.1:8080?key=all&name=%s">全部已阅</a>'%urllib.quote(name)
		body+='''<h2><a href='%s'>%s</a></h2>
				<div class="well well-small">
                <table class="table table-hover">
                <tbody>
	    	     <tr><td>标题</td><td align="center">日期</td><td>操作</td></tr>
	             %s
	    	     <tr><td></td><td align="center"></td><td>%s</td></tr>
                </tbody>
                </table>
				</div>'''% (source['url'],name,link_list,link_outAll)

	return '''
                <html>
                    <head>
                        <meta charset="utf-8">
                        <title>新闻聚合网站</title>
                        <link href="//cdnjs.bootcss.com/ajax/libs/twitter-bootstrap/2.3.1/css/bootstrap.min.css" rel="stylesheet">
                        <style>
                            body {
                                width: 80em;
                                margin: 0 auto;
                            }
                            .table-hover tbody tr:hover > td,
                                .table-hover tbody tr:hover > th {
                                background-color: #D2DAFF;
                            }
                            a:visited { color: red; }
                        </style>
                    </head>
                    <body>
					%s
                    </body>
                    </html>
                ''' %body

def out_of_date(rs,name,key):
	rs.hdel(name,key)
	rs.hdel(name+'_date',key)
	rs.sadd(name+'_outDate',key) # srem for removing

class HttpHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		rs=redis.Redis()
		qs=parse_qs(urlparse(self.path).query)
		# 对于已阅的链接，删除其在redis里的表项
		if qs:
			key=qs['key'][0]
			name=urllib.unquote(qs['name'][0]) # ？？能解析出utf-8？
			logging.warning(name)
			if key=='all':
				# 全部清空
				for key1 in rs.hkeys(name):
					out_of_date(rs,name,key1)
			else:
				out_of_date(rs,name,key)
			logging.warning(key+' is removed from redis')
			self.send_response(301) #!!!重定向
			self.send_header("Location","http://127.0.0.1:8080") #!!!重定向
			self.end_headers()
		else:
			self.send_response(200) 
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(generate_page(rs))
		return
