import copy
import re
from urllib.parse import urlparse,quote,unquote
import config
from checker import checker
from config import xsschecker
from filterChecker import filterCheccker
from generator import generator
from htmlparser import htmlParser
from requester import requester
from config import headers,minEfficiency



config.globalVaribales['headers']=headers
config.globalVaribales['checkedScripts']=set()
config.globalVariables['checkedForms']={}

#扫描的参数设置 通过GUI 传参进来
target=''
path=''
jsonData=''
paramData=''
proxy=''
recursive=''#判断是否递归
threadCount=''
skipDOM=''#
timeout=''
encode=''



if path:#如果target中包含路径
    paramData=converter(target,target)#将路径中的参数提取出来
elif jsonData:
    headers['Content-type']='application/json'
    paramData=converter(paramData)#将paramData转换成json格式

encoding=base64 if encode and encode=='base64' else False

if not proxy:
    config.proxies={}

scan(target,paramData,encoding,headers,delay,timeout,skipDOM,find,skip)








def scan(target,paramData,encoding,headers,delay,timeout,path,jsonData):
    GET,POST=(False,True) if paramData else (True,False)
    #如果用户输入的入口主URL不是以http/https开头，会进行处理
    if not target.startswith('http'):
        try:
            response=requester('https://'+target,{},headers,GET,delay,timeout)
            target='https://'+target
        except:
            target='http://'+target
    response=requester(target,{},headers,GET,delay,timeout,jsonData,path).text#得到入口target的response


    host=urlparse(target).netloc#将host提取出来
    url=getUrl(target,GET)
    params=getParams(target,paramData,GET,jsonData,path)#将target中的参数提取出来
    # if find:
    #     params=get_forms(url,GET,headers,delay,timeout)

    for paraName in params.keys():
        paramsCopy=copy.deepcopy(params)

        if encoding:
            paramsCopy[paramName]=encoding(xsschecker)
        else:
            paramsCopy[parasName]=xsschecker
        response=requester(url,paramsCopy,headers,GET,delay,timeout,jsonData,path)
        occurences=htmlParser(response,encoding)#获得输出点得上下文环境
        positions=occurences.keys()

        if not occurences:
            print('No reflection found')
            continue
        else:
            print('Reflections found:%i' %len(occurences))

        #filterChecker函数检查每个输出位置是否过滤了> < " ' //这些特殊符号
        efficiencies=filterCheccker(url,paramsCopy,headers,GET,delay,occurences,timeout,encoding)#对过滤字符的打分列表

        vectors=generator(occurences,response.text)#生成payload
        total=0
        for v in vectors.values():
            total+=len(v)#总共生成了多少条payload
        if total==0:
            print('No vectors were crafted.')
            continue
        progress=0
        for confidence,vects in vectors.items():
            for vect in vects:
                if config.globalVariables['path']:
                    vect=vect.replace('/','%2F')#如果用户设置在url路径中插入payload

                loggerVector=vect
                progress+=1

                if not GET:
                    vect=unquote(vect)
                efficiencies=checker(url,paramData,headers,GET,delay,vect,positions,timeout,encoding)
                if not efficiencies:
                    for i in range(len(occurences)):
                        efficiencies.append(0)
                        bestEfficiency=max(efficiencies)

                if bestEfficiency==100 or (vect[0]=='||' and bestEfficiency>=95):
                    print("Payload:%s" %loggerVector)
                    print("Efficiency:%s Confidence:%s" %(bestEfficiency,confidence))
                elif bestEfficiency>minEfficiency:
                    print("Payload:%s" %loggerVector)
                    print("Efficiency:%s Confidence:%s" %(bestEfficiency,confidence))









