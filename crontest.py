#!/usr/local/bin/python3
# coding:utf-8
import requests
from bs4 import BeautifulSoup

response = requests.get("http://www.edianzu.cn/")
soup = BeautifulSoup(response.text,'html.parser')
print('test cron')
print(soup.find("a"))
