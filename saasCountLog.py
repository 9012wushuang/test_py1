#!/usr/local/bin/python3
# coding:utf-8
import sys

sys.path.append(r"/data/bifenghui/python3")
import saasDb as sDb
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')


def rootMerge():
    listResult = []
    # get root company id
    companyIdList = sDb.getSomeRootCompanyIds()
    mergeCount = merge()
    pvDict = mergeCount.get('companyIpDict')
    uvDict = mergeCount.get('companyUvDict')
    for companyId in companyIdList:
        subsidiaryDict = {}
        subsidiaryCompanyIds = sDb.getIdsByRootCompanyId(companyId)
        allPv = 0
        allUv = 0
        for keyId in subsidiaryCompanyIds:
            pv = pvDict.get(str(keyId))
            if pv is None:
                pv = 0
            uv = uvDict.get(str(keyId))
            if uv is None:
                uv = 0
            dict = {str(keyId): {'pv': pv, 'uv': uv}}
            subsidiaryDict.update(dict)
            allPv = allPv + pv
            allUv = allUv + uv

        tempUvPvList = []
        tempUvPvList.append(subsidiaryDict)

        # output data
        dictPv = {'allPv': allPv}
        dictUv = {'allUv': allUv}
        dictSall = {'rootDict': subsidiaryDict}

        temp1 = {}
        temp1.update(dictPv)
        temp1.update(dictUv)
        temp1.update(dictSall)
        tempDictBut = {companyId: temp1}

        listResult.append(tempDictBut)

    return listResult


def getSystemPvUv():
    mergeCount = merge()
    systemUvPv = mergeCount.get('uvPvdict')
    return systemUvPv


def pcLogCount():
    jsonPathIpWeb = '/data/log/asset/asset-web/countIpUvPvVv.log'
    ipList = []
    uvList = []
    companyIpDict = {}
    companyUvDict = {}
    companyUvDict_count = {}  # company uv

    jsonFileIpWeb = open(jsonPathIpWeb, 'r')
    try:
        for lineIpWeb in jsonFileIpWeb:
            if lineIpWeb != '\n':
                listIpWeb = lineIpWeb.split(',')
                for data in listIpWeb:
                    newData = data.split('=')[1]
                    if data.find('ip') != -1:
                        ipList.append(newData)
                    if data.find('userId') != -1:
                        if newData not in uvList:
                            uvList.append(newData)
                    if data.find('uvCUids') != -1:
                        if newData in companyUvDict:
                            value = companyUvDict.get(newData)
                            value = int(value) + 1
                            companyUvDict[newData] = value
                        else:
                            dict = {newData: 1}
                            companyUvDict.update(dict)
                    if data.find('companyId') != -1:
                        if newData in companyIpDict:
                            value = companyIpDict.get(newData)
                            value = value + 1
                            companyIpDict[newData] = value
                        else:
                            if newData != 'null':
                                dict = {newData: 1}
                                companyIpDict.update(dict)

        for key, value in companyUvDict.items():
            key = key.split('-')[0]
            if key in companyUvDict_count:
                value = companyUvDict_count.get(key)
                value = int(value) + 1
                companyUvDict_count[key] = value
            else:
                dict = {key: 1}
                companyUvDict_count.update(dict)

        uvPvdict = {'pv': len(ipList), 'uv': len(uvList) - 1}
    finally:
        jsonFileIpWeb.close()
    webCount = {'uvPvdict': uvPvdict, 'companyIpDict': companyIpDict, 'companyUvDict_count': companyUvDict_count}
    return webCount


def test():
    jsonPathIpApi = '/data/log/asset/asset-web-api/countIpUvPvVv.log'

    ipList = []
    uvList = []
    companyIpDict = {}
    companyUvDict = {}
    companyUvDict_count = {}  # company uv

    jsonFileIpApi = open(jsonPathIpApi, 'r')
    try:
        for lineIpApi in jsonFileIpApi:
            if lineIpApi != '\n':
                listIpApi = lineIpApi.split(',')
                for data in listIpApi:
                    newData = data.split('=')[1]
                    if data.find('ip') != -1:
                        ipList.append(newData)
                    if data.find('userId') != -1:
                        if newData not in uvList:
                            uvList.append(newData)
                    if data.find('uvCUids') != -1:
                        if newData in companyUvDict:
                            value = companyUvDict.get(newData)
                            value = int(value) + 1
                            companyUvDict[newData] = value
                        else:
                            dict = {newData: 1}
                            companyUvDict.update(dict)
                    if data.find('companyId') != -1:
                        if newData in companyIpDict:
                            value = companyIpDict.get(newData)
                            value = value + 1
                            companyIpDict[newData] = value
                        else:
                            if newData != 'null':
                                dict = {newData: 1}
                                companyIpDict.update(dict)
        for key, value in companyUvDict.items():
            key = key.split('-')[0]
            if key in companyUvDict_count:
                value = companyUvDict_count.get(key)
                value = int(value) + 1
                companyUvDict_count[key] = value
            else:
                dict = {key: 1}
                companyUvDict_count.update(dict)
        uvPvdict = {'pv': len(ipList), 'uv': len(uvList) - 1}
    finally:
        jsonFileIpApi.close()

    apiCount = {'uvPvdict': uvPvdict, 'companyIpDict': companyIpDict, 'companyUvDict_count': companyUvDict_count}

    return apiCount


def merge():
    apiCount = test()
    webCount = pcLogCount()
    mergeCount = {}

    uvPvdictWeb = apiCount.get('uvPvdict')
    uvPvdictApi = webCount.get('uvPvdict')
    uvPvdict = {}
    pv = uvPvdictWeb.get('pv') + uvPvdictApi.get('pv')
    uv = uvPvdictWeb.get('uv') + uvPvdictApi.get('uv')
    uvPvdict = {'pv': pv, 'uv': uv}

    companyIpDictWeb = apiCount.get('companyIpDict')
    companyIpDictApi = webCount.get('companyIpDict')
    companyIpDict = {}
    for key, value in companyIpDictWeb.items():
        if key in companyIpDict:
            vl = companyIpDict.get(key)
            companyIpDict[key] = value + vl
        else:
            tempDict = {key: value}
            companyIpDict.setdefault(key, value)

    for key, value in companyIpDictApi.items():
        if key in companyIpDict:
            vl = companyIpDict.get(key)
            companyIpDict[key] = value + vl
        else:
            tempDict = {key: value}
            # logging.debug(tempDict)
            # logging.debug(companyIpDict)
            companyIpDict.update(tempDict)

    companyUvDictWeb = apiCount.get('companyUvDict_count')
    companyUvDictApi = webCount.get('companyUvDict_count')
    companyUvDict = {}
    for key, value in companyUvDictWeb.items():
        if key in companyUvDict:
            vl = companyUvDict.get(key)
            companyUvDict[key] = value + vl
        else:
            tempDict = {key: value}
            companyUvDict.setdefault(key, value)

    for key, value in companyUvDictApi.items():
        if key in companyUvDict:
            vl = companyUvDict.get(key)
            companyUvDict[key] = value + vl
        else:
            tempDict = {key: value}
            companyUvDict.update(tempDict)
    mergeCount = {'uvPvdict': uvPvdict, 'companyIpDict': companyIpDict, 'companyUvDict': companyUvDict}
    return mergeCount
