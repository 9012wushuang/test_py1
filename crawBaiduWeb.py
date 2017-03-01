#!/usr/local/bin/python3
# coding:utf-8

import sys
import requests
import webbrowser
import logging
import bs4

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')


def testConnectBaidu():
    response = requests.get('https://www.baidu.com')

    logging.debug(response.raise_for_status())

    if response.raise_for_status():
        logging.debug('connect ok')

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # playFile = open('/data/bifenghui/web.txt', 'wb')
    for chunk in response.iter_content(10000):
        print(chunk.decode('utf-8'))
        # webbrowser.open(soup)



testConnectBaidu()
