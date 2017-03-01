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
    res = requests.get('https://www.google.com/search?q=' + ' '.join(sys.argv[1:]))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    linkElems = soup.select('.r a')
    logging.debug(len(linkElems))
    numopen = min(5, len(linkElems))
    for i in range(numopen):
        logging.debug(linkElems[i])
        webbrowser.open('https://google.com'+linkElems[i].get('href'))
    logging.debug('search result end...')

searchGoole()