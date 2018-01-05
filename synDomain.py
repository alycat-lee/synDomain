#-*- coding: utf8 -*-
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
import http
import urllib2

class SyncLocalDomain():
    def __init__(self):
        self.recordIp = None
        self.recordId = None
        with open('ali.json') as fp:
            jsonfile = json.loads(fp.read())
        aliConfig = jsonfile.get('ali')
        self.config = jsonfile.get('local')
        self.client = AcsClient(    
            aliConfig.get('aki'), 
            aliConfig.get('aks'), 
            aliConfig.get('akz')
        )
        self.getRealIp()
        self.getDomainInfoFromWeb()

    #获取阿里云域名解析记录
    def getDomainInfoFromWeb(self):
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_DomainName(self.config.get('domain'))
        response = json.loads(self.client.do_action_with_exception(request))
        for lines in response['DomainRecords']['Record']:
            if lines['RR'] == self.config.get("record") and lines['Type'] == self.config.get("type"):
                self.recordId = lines['RecordId']
                self.recordIp = lines['Value']

    #通过ip138获取本机公网IP
    def getRealIp(self):
        html_code = urllib2.urlopen('http://2017.ip138.com/ic.asp').read()
        hp = http.LocalIP()
        hp.feed(html_code)
        hp.close()
        self.realIp = hp.content

    #更新阿里云域名解析信息
    def updateDomainInfo(self):
        if(self.recordIp is not None): 
            if(self.realIp != self.recordIp):
                request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
                request.set_RecordId(self.recordId)
            else:
                return 0    
        else:
            #阿里云不存在该解析时 新增解析记录
            request = AddDomainRecordRequest.AddDomainRecordRequest()
            request.set_DomainName(self.config.get('domain'))
        request.set_Type(self.config.get("type"))
        request.set_Value(self.realIp)
        request.set_RR(self.config.get('record'))
        response = json.loads(self.client.do_action_with_exception(request))    
        return 1



if __name__ == '__main__':
    result = SyncLocalDomain().updateDomainInfo()
    if(result == 1):
        print 'ok'
    else:
        print 'no need'
