import requests
import re
import thread
import random
from requester import requester
from htmlparser import htmlParser

def crawl(scheme,host,main_url,form,headers,delay,timeout):
    if form:#这个form是一个表单，应该是从返回页面中提取出来的表单集合
        for each in form.values():
            url=each['action']
            if url:
                if url.startswith(main_url):
                    pass
                elif url.startswith('//') and url[2:].startswith(host):
                    url=scheme+'://'+url[2:]
                elif url.startswith('/'):
                    url=scheme+'://'+host+url
                if url not in config.globalVariables['checkedForms']:
                    config.globalVariables['checkedForms'][url]=[]
                method=each['method']
                GET=True if method=='get' else False
                inputs=each['inputs']#一个form表单中的input标签的集合
                paramData={}
                for one in inputs:
                    paramData[one['name']]=one['value']
                    for paramName in paramData.keys():
                        if paramName not in config.globalVariables['checkedForms'][url]:
                            config.globalVariables['checkedForms'][url].append(paramName)
                            paramsCopy=copy.deepcopy(paramData)
                            paramsCopy[paramName]=xsschecker
                            response=requester(url,paramsCopy,headers,GET,delay,timeout)#发送GET请求
                            occurences=htmlParser(response,encoding)#返回的是html网页中输出点的上下文信息
                            positions=occurences.keys()#注入点位置
                            #模糊测试，判断xss漏洞的匹配度？？
                            efficiences=filterChecker(url,paramsCopy,headers,GET,delay,occurences,timeout,encoding)
                            vectors=generator(occurences,response.text)#生成攻击向量？？
                            #存储攻击向量的数据结构
                            payloads=[]
                            if vectors:
                                for confidence,vects in vectors.items():
                                    try:
                                        payload=list(vects)[0]
                                        print(payload)
                                        payloads.append(payload)
                                        break
                                    except IndexError:
                                        pass








