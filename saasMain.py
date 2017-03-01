#!/usr/local/bin/python3
# coding:utf-8
import sys

sys.path.append(r"/data/bifenghui/python3")
import saasDb as sDb
import json
# import saasSendMail as sSendMail
import saasSendMailV1 as tsSendMail
import saasCountLog as SCLog
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')


def parseJson():
    jsonPath = '/data/bifenghui/python3/count.txt'
    companyCountDataList = []  # company data count
    jsonFile = open(jsonPath, 'r')
    try:
        subsidiaryIdInfosDict = {}
        line = jsonFile.readlines()
        i = 0
        for data in line:
            if data != '\n':
                data = json.loads(data)
                if len(data) > 0:
                    allCount = json.loads(data[0]['assetOther'])['all']['count']
                    addCount = json.loads(data[0]['assetOther'])['add']['count']
                    receiveCount = json.loads(data[0]['assetStatus'])['receive']['count']
                    borrowCount = json.loads(data[0]['assetStatus'])['borrow']['count']
                    freeCount = json.loads(data[0]['assetStatus'])['free']['count']
                    companyId = json.loads(str(data[0]['companyId']))
                    rootCompanyId = json.loads(str(data[0]['rootCompanyId']))
                    dict = {companyId: [{'allCount': allCount}, {'addCount': addCount}, {'receiveCount': receiveCount},
                                        {'borrowCount': borrowCount}, {'freeCount': freeCount}]}

                    if rootCompanyId in subsidiaryIdInfosDict.keys():
                        all_list = subsidiaryIdInfosDict.get(rootCompanyId)[0].get('all')
                        for count_dict in all_list:
                            for key, value in count_dict.items():
                                count = count_dict.get(key)
                                if key == 'allCount':
                                    count = str(int(count) + int(allCount))
                                if key == 'addCount':
                                    count = str(int(count) + int(addCount))
                                if key == 'receiveCount':
                                    count = str(int(count) + int(receiveCount))
                                if key == 'borrowCount':
                                    count = str(int(count) + int(borrowCount))
                                if key == 'freeCount':
                                    count = str(int(count) + int(freeCount))
                                count_dict[key] = count
                        subsidiaryIdInfosDict.get(rootCompanyId)[0].setdefault('all', count_dict)
                        subsidiaryIdInfosDict.get(rootCompanyId).append(dict)
                    else:
                        allDict = {
                            'all': [{'allCount': dict.get(companyId)[0].get('allCount')},
                                    {'addCount': dict.get(companyId)[1].get('addCount')},
                                    {'receiveCount': dict.get(companyId)[2].get('receiveCount')},
                                    {'borrowCount': dict.get(companyId)[3].get('borrowCount')},
                                    {'freeCount': dict.get(companyId)[4].get('freeCount')}]}
                        # logging.info(allDict)
                        list = [allDict, dict]
                        tempDict = {rootCompanyId: list}
                        subsidiaryIdInfosDict.update(tempDict)
                    companyCountDataList.append(dict)
    finally:
        jsonFile.close()

    # logging.debug(subsidiaryIdInfosDict)
    uvPvdict = SCLog.getSystemPvUv()
    result = SCLog.rootMerge()
    print('统计数据完成...')
    # sSendMail.sendMail(uvPvdict, result, companyCountDataList)
    tsSendMail.sendMail(uvPvdict, result, subsidiaryIdInfosDict)


def inputPath():
    try:
        countDate = time.strftime("%Y-%m-%d", time.localtime())
        # logging.debug(countDate)
        writeFilePath = '/data/bifenghui/python3/count.txt'
        allCountCompanyId = sDb.getAllCountCompanyId()
        sDb.getCompanies(countDate, writeFilePath, allCountCompanyId)
    except:
        print('your inputStr are error,please check')


print('start count data...')
inputPath()
parseJson()
print('count data end...')
