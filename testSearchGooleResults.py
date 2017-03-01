#!/usr/local/bin/python3
# coding:utf-8

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
import requests
import sys
import webbrowser
import bs4


def searchGoole():
    logging.debug('search result...')
    # res = requests.get('https://www.google.com/search?q=' + ' '.join(sys.argv[1:]))
    res = requests.get('https://www.baidu.com')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # logging.debug(type(soup))
    # logging.debug(soup)
    linkElems = soup.select('a')
    # logging.debug(len(linkElems))
    # logging.debug(type(linkElems))
    for value in linkElems:
        print('----')
        # logging.debug(value.get('href'))
    # numopen = min(5, len(linkElems))
    # for i in range(numopen):
    #     logging.debug(linkElems[i])
    #     webbrowser.open('https://google.com'+linkElems[i].get('href'))
    # soup.select('#kw')
    res1 = requests.get('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=' + ' '.join(sys.argv[1:]))
    print(res1.raise_for_status())
    soup1 = bs4.BeautifulSoup(res1.text, 'html.parser')
    logging.debug(soup1)
    # webbrowser.open(soup1)


logging.debug('search result end...')

searchGoole()
