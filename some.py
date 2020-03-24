from get_form import get_form
import re
from urllib.parse import urlparse
import config
import copy
from htmlparser import htmlParser
from filterChecker import filterChecker
from generator import generator
from config import headers,delay,timeout,xsschecker
from requester import requester
import requests
from scan import scan


#crawl(scheme,main_url,host,form,headers,delay,timeout)
schmem='http'
main_url='http://127.0.0.1/message_box/MessageBoard.php'
scheme=urlparse(main_url).scheme
print(scheme)
host=urlparse(main_url).netloc
print(host)
timeout=10

# res1=crawl(scheme,main_url,host,form,headers,delay,timeout)

res=requests.get(main_url).text
form=get_form(res)
print(form)
# def crawl(scheme,main_url,host,form,headers,delay,timeout):
#     show_message={'info':'the crawling results are:'}
#     if form:#这是form是一个表单，应该是从返回页面中提取出来的表单的集合
#         for each in form.values():
#             url=each['action']
#             if url:
#                 if url.startswith(main_url):
#                     pass
#                 elif url.startswith('//') and url[2:].startswith(host):
#                     url=scheme+'://'+url[2:]
#                 elif url.startswith('/'):
#                     url=scheme+'://'+host+url
#                 if url not in config.globalVariables['checkedForms']:
#                     config.globalVariables['checkedForms'][url]=[]#如果url没有测试过，则加入已测试队列
#
#                 method=each['method']
#                 GET=True if method=='get' else False
#                 inputs=each['inputs']#一个form表单中的input标签的集合
#                 paramData={}
#                 for one in inputs:
#                     paramData[one['name']]=one['value']
#                     for paramName in paramData.keys():
#                         if paramName not in config.globalVariables['checkedForms'][url]:
#                             config.globalVariables['checkedForms'][url].append(paramName)
#                             paramsCopy=copy.deepcopy(paramData)
#                             paramsCopy[paramName]=xsschecker
#                             response=requester(url,paramsCopy,headers,GET,delay,timeout,info='path')
#                             occurences=htmlParser(response,encoding)#返回的是html网页中输出点的上下文信息
#                             positions=occurences.keys()#注入点的位置
#                             #模糊测试，判断特定字符的过滤情况
#                             efficiences=filterChecker(url,paramsCopy,headers,GET,occurences,timeoutmencoding)
#                             vectors=generator(occurences,response.text)
#                             payloads=[]
#                             if vectors:
#                                 for confidence,vects in vectors.items():
#                                     try:
#                                         payload=list(veccts)[0]
#                                         res='Vulberable webpage:%s' %url+'Vector for %s:%s' %(paramName,payload)
#                                         show_message.add(res)
#                                         print(payload)
#                                         payloads.append(payload)
#                                         break
#                                     except:
#                                         pass
#                             else:
#                                 pass
#     return show_message

res1=crawl(scheme,main_url,host,form,headers,delay,timeout)
print(res1)
































# import copy
#
# def replaceValue(mapping, old, new, strategy=None):
#     """
#     Replace old values with new ones following dict strategy.
#
#     The parameter strategy is None per default for inplace operation.
#     A copy operation is injected via strateg values like copy.copy
#     or copy.deepcopy
#
#     Note: A dict is returned regardless of modifications.
#     """
#     anotherMap = strategy(mapping) if strategy else mapping
#     if old in anotherMap.values():
#         for k in anotherMap.keys():
#             if anotherMap[k] == old:
#                 anotherMap[k] = new
#     return anotherMap
#
# checkString='ssss'
# params={'name':'liu','pass':'liu'}
# xsschecker='liu'
# print(replaceValue(params,xsschecker,checkString,copy.deepcopy))
#


















