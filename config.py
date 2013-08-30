# -*- coding=utf-8 -*-

import re

# 每隔10min抓取一次
LOG_PATH='/home/mashu/log/infoCollection.log'
INTERVAL={'hour':'*','min':'*/10','sec':'0'}
SOURCE=(
		{
			'name':'软件学院-学生周知',
			'root':'http://ssdut.dlut.edu.cn',
			'url':'http://ssdut.dlut.edu.cn/index.php/News/student.html',
			'href_form':re.compile(r'/index\.php/News/\d+\.html'),
			'date_form':re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}'),
			'date_loc':'after'
		},
		{
			'name':'软件学院-实习就业信息',
			'root':'http://ssdut.dlut.edu.cn', 
			'url':'http://ssdut.dlut.edu.cn/index.php/Career/index/p/1/',
			'href_form':re.compile(r'/index\.php/Career/\d+.html'),
			'date_form':re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}'),
			'date_loc':'after'
		},
		{
			'name':'创新学院-竞赛新闻',
			'root':'http://chuangxin.dlut.edu.cn/', #!!
			'url':'http://chuangxin.dlut.edu.cn/SecondPage_News.aspx?Type=6',
			'href_form':re.compile(r'show\.aspx\?id=\d+'),
			'date_form':re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}'),
			'date_loc':'after'
		},
		{
			'name':'研究生院-通知和新闻',
			'root':'http://gs.dlut.edu.cn/', #!!
			'url':'http://gs.dlut.edu.cn/index.asp',
			'href_form':re.compile(r'showdetail\.asp\?id=\d+'),
			'date_form':re.compile(r'[\d]{2}-[\d]{2}-[\d]{2}'),
			'date_loc':'before'
		},
		{
			'name':'大工就业网-实习生招聘',
			'root':'http://career.dlut.edu.cn/NetInfo/', 
			'url':'http://career.dlut.edu.cn/NetInfo/NetInfoMore.aspx?Hid=1&Tid=4',
			'href_form':re.compile(r'NetInfoDetail\.aspx\?id=\d+'),
			'date_form':re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}'),
			'date_loc':'after'
		},
		{
			'name':'大工就业网-需求信息',
			'root':'http://career.dlut.edu.cn/XuQiuXinXi/', 
			'url':'http://career.dlut.edu.cn/XuQiuXinXi/XuQiuXinXiMore.aspx',
			'href_form':re.compile(r'XuQiuXiangXiXinXi\.aspx\?id=\d+'),
			'date_form':re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}'),
			'date_loc':'after'
		},
		{
			'name':'大工就业网-招聘会信息',
			'root':'http://career.dlut.edu.cn/ZhuanChangZhaoPinHui/', 
			'url':'http://career.dlut.edu.cn/ZhuanChangZhaoPinHui/ZhaoPinHuiMore.aspx',
			'href_form':re.compile(r'ZhaoPinHuiXiangXiXinXi\.aspx\?id=\d+'),
			'date_form':re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}'),
			'date_loc':'after'
		},
		)
