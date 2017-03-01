#!/usr/local/bin/python3
# coding:utf-8

import sys

sys.path.append(r"/data/bifenghui/python3")
import pymysql
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')

host = '123.57.6.101'
user = 'edianzu_dev'
password = 'aedianazu321'
db = 'db_cloud_assets'
port = 3306


def getSomeRootCompanyIds():
    rootDataList = []
    try:
        connection = pymysql.connect(host, user, password, db, port, charset='utf8')
        cursor = connection.cursor()
        sql = 'select id from asset_company where  id in (22,25,2786,2852,2827)'
        count = cursor.execute(sql)
        data = cursor.fetchall()
        for value in list(data):
            rootDataList.append(value[0])
    finally:
        connection.close()
    return rootDataList


def getRootCompanyName(companyId):
    # db sql
    try:
        connection = pymysql.connect(host, user, password, db, port, charset='utf8')
        cursor = connection.cursor()
        sql_1 = 'select parent_company_id from asset_company where id = %s'
        sql_2 = 'select name from asset_company where id = %s'
        count = cursor.execute(sql_1, [companyId])
        data = cursor.fetchone()  # get one data
        if list(data)[0] is not None:
            cursor.execute(sql_2, [list(data)[0]])
            data_new = cursor.fetchone()
            rootCompanyName = list(data_new)[0]
        else:
            cursor.execute(sql_2, [companyId])
            data_new = cursor.fetchone()
            rootCompanyName = list(data_new)[0]
        connection.commit()
        return rootCompanyName
        # except:
        # print('Mysql connect fail...')
    finally:
        connection.close()


def getAllCountCompanyId():
    allCountCompanyId = []
    # db sql
    try:
        connection = pymysql.connect(host, user, password, db, port, charset='utf8')
        cursor = connection.cursor()
        sql = 'select id from asset_company where name not like "%测试%" and name not like "%ceshi%" order by ' \
              'parent_company_id '
        count = cursor.execute(sql)
        data = cursor.fetchall()
        connection.commit()
        listData = list(data)
        if len(data) > 0:
            for i in range(len(data)):
                allCountCompanyId.append(listData[i][0])
                # print(allCountCompanyId)
    except:
        print('Mysql connect fail...')
    finally:
        connection.close()
        # allCountCompanyId.append()
    return allCountCompanyId


def getIdsByRootCompanyId(rootCompanyId):
    jsonData = []
    try:
        connection = pymysql.connect(host, user, password, db, port, charset='utf8')
        cursor = connection.cursor()
        sql = 'select id from asset_company where  parent_company_id = %s'
        count = cursor.execute(sql, [rootCompanyId])
        data = cursor.fetchall()
        connection.commit()
        listData = list(data)

        jsonData.append(rootCompanyId)
        if len(data) > 0:
            for i in range(len(data)):
                jsonData.append(listData[i][0])

    except:
        print('Mysql connect fail...')
    finally:
        connection.close()

    return jsonData


def getCompanyName(companyId):
    try:
        connection = pymysql.connect(host, user, password, db, port, charset='utf8')
        cursor = connection.cursor()
        sql = 'select name from asset_company where id = %s'
        count = cursor.execute(sql, [companyId])
        data = cursor.fetchone()
        connection.commit()
        if data == '':
            return 'please get help from edianzu saas '
        else:
            return data[0]
    except:
        print('MySql connect fail...')
    finally:
        connection.close()


def getData(companyId, dataTime):
    jsonData = []
    try:
        connection = pymysql.connect(host, user, password, db, port, charset='utf8')
        cursor = connection.cursor()
        sql = 'select asset_status,asset_source,asset_other,company_id,root_company_id,date,month_begin_hand_end from asset_basic_data where company_id = %s and date = %s order by id desc limit 1'
        count = cursor.execute(sql, [companyId, dataTime])
        # data = cursor.fetchone()
        data = cursor.fetchall()
        for d in data:
            if (d):
                result = {}
                result['assetStatus'] = d[0]
                result['assetSource'] = d[1]
                result['assetOther'] = d[2]
                result['companyId'] = d[3]
                result['rootCompanyId'] = d[4]
                jsonData.append(result)
                connection.commit()
    except:
        print('MySql connect fail...')
    finally:
        connection.close()
    jsonDataResult = json.dumps(jsonData, ensure_ascii=False)
    return jsonDataResult


def getCompanies(countDate, writeFilePath, companyList):
    dataTime = countDate  # count date
    for i in range(len(companyList)):
        fo = open(writeFilePath, 'r+')
        if i == 0:
            fo.truncate()
        companyId = int(companyList[i])
        result = getData(companyId, dataTime)
        fo.readlines()
        fo.writelines('\n')
        if len(result) != 0:
            fo.writelines(result)
        fo.flush()
        fo.close()

# getCompanies('2017-02-23','/Users/bifenghui/work/edianzu/count20170223.txt',[2786,2852])
# print(getCompanyName(2786))
# print(getIdsByRootCompanyId(2786))
# print(getAllCountCompanyId())
# print(getRootCompanyName(2825))
# print(getIdsByRootCompanyId(48))
