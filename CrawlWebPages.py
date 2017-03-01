#!/usr/local/bin/python3
# coding:utf-8

import sys
import logging
import requests
import bs4
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')


def crawWeb():
    logging.debug('开始-抓取网页')
    res = requests.get('http://www.edianzu.cn')
    logging.debug(type(res))
    try:
        res.raise_for_status()
    except Exception as exc:
        print(exc)
        logging.error(exc)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    type(soup)
    playFile = open('/data/bifenghui/web.txt', 'wb')
    for chunk in res.iter_content(100000):
        playFile.write(chunk)
    logging.debug('抓取网页-结束')


crawWeb()
