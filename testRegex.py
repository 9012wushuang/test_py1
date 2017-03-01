#!/usr/local/bin/python3
# coding:utf-8

import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')


def testRegex(str):
    testRegex = re.compile(r'''(
(\d{3}|\(\d{3}\))？ # are code
)''', re.VERBOSE)

    value = testRegex.search(str)
    if value != None:
        logging.debug(value.group())
        logging.debug(value.groupdict())
        logging.debug(value.groups())
    else:
        logging.debug(value)


testRegex('12345-6789')
