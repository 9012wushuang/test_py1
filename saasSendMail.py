#!/usr/local/bin/python3
# coding:utf-8

import sys

sys.path.append(r"/data/bifenghui/python3")
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import saasDb as sDb
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')

host = 'smtp.exmail.qq.com'
port = 25  # 25 为 SMTP 端口号
mail_user = 'bifenghui@edianzu.cn'
mail_pass = 'asnMM5396362'

sender = 'bifenghui@edianzu.cn'
receivers = ['bifenghui@edianzu.cn']


def sendMail(uvPvMessage, listResult, companyCountDataMessage):
    print("开始发送邮件...")

    tr1 = '<tr><td>pv and uv纬度</td><td>计数</td></tr>';
    tr2 = '<tr><td>root公司</td><td>公司名称</td><td>资产总数包括租赁及采购资产</td><td>新增数量</td><td>领用数量</td><td>借用数量</td><td>空闲数量</td></tr>';

    resultData = ''
    for result in listResult:
        rootCompanyId = list(result.keys())[0]
        dictPvUv = result.get(rootCompanyId)
        allPv = dictPvUv.get('allPv')
        allUv = dictPvUv.get('allUv')
        rootDict = dictPvUv.get('rootDict')

        data = '<span></span>'
        data = data + '<table border="1px"  style="border-collapse:collapse" cellpadding="0" cellspacing="0" width="100%">'
        data = data + '<tr bgcolor="#CCD1D1"><td>root公司</td><td>allpv</td><td>alluv</td></tr>'
        data = data + '<tr><td>' + sDb.getCompanyName(rootCompanyId) + '</td><td>' + str(allPv) + '</td><td>' + str(
            allUv) + '</td></tr>'
        data = data + '<tr bgcolor="#D4EFDF"><td>公司</td><td>pv</td><td>uv</td></tr>'
        for key, value in rootDict.items():
            pv = value.get('pv')
            uv = value.get('uv')
            data = data + '<tr><td>' + sDb.getCompanyName(key) + '</td><td>' + str(pv) + '</td><td>' + str(
                uv) + '</td></tr>'
        data = data + '</table>'

        resultData = resultData + data

    # logging.debug(companyCountDataMessage)
    companyCountDataStr = ''
    for data in companyCountDataMessage:
        dataTr = ''
        dataStr = ''
        keyCompanyId = 0
        for keyDict, valueDict in data.items():
            keyCompanyId = keyDict
            for cstr in valueDict:
                for key, value in cstr.items():
                    dataStr = dataStr + '<td>' + value + '</td>'
        # dataTr = '<tr><td>'+sDb.getRootCompanyName(keyCompanyId)+'</td><td>'+sDb.getCompanyName(keyCompanyId)+'</td>'+dataStr+'</tr>'
        dataTr = '<tr><td>' + sDb.getRootCompanyName(keyCompanyId) + '</td><td>' + sDb.getCompanyName(
            keyCompanyId) + '</td>' + dataStr + '</tr>'
        companyCountDataStr = companyCountDataStr + dataTr
    try:
        message = '''
        <HTML><HEAD>
        <TITLE>资产实施关注点</TITLE>
        </HEAD>
        <BODY >
        <span>系统uv和pv</span>
        <table border='1px' style='border-collapse:collapse' cellpadding='0' cellspacing='0' width='100%'>
        ''' + tr1 + '''
        <tr><td>pv</td><td>''' + str(uvPvMessage.get('pv')) + '''</td></tr>
        <tr><td>uv</td><td>''' + str(uvPvMessage.get('uv')) + '''</td></tr>
        </table>
        <span>公司pvUv</span>
        ''' + resultData + '''
        <span>公司资产数据统计</span>
        <table border='1px'  style='border-collapse:collapse' cellpadding='0' cellspacing='0' width='100%'>
        ''' + tr2 + '''
        ''' + companyCountDataStr + '''
        </table>
        </BODY>
        </HTML>
        '''
        message = MIMEText(message, 'html', 'utf-8')
        message['From'] = Header('bifenghui@edianzu.cn', 'utf-8')
        message['To'] = Header("易点租saas", 'utf-8')
        subject = '资产实施关注点'
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = smtplib.SMTP()
        smtpObj.connect(host, port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
