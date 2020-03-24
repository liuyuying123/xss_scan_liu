import re
import json
import queue

#Queue.empty():判断队列是否为空，若为空则返回False，否则返回True


wei_url=queue.Queue()#未爬取的URL队列
yi_url=queue.Queue()#已经爬过的URL队列
error_url=queue.Queue()#出现错误的URL队列



def get_url():
    if not wei_url.empty():
        return wei_url.get()#得到队首的url
    else:
        return 0

def error_url_append(url):#将发生错误的URL加入到error_url对列中
    error_url.put(url)
    return 0

def wei_url_append(url):#将从网页中解析出来的url加入到未爬取的wei_url队列中
    wei_url.put(url)
    return 0

def yi_url_append(url):#将已经爬取过的URL加入到yi_url队列中
    yi_url.put(url)
    return 0




def extractScripts(response):
    scripts = []
    matches = re.findall(r'(?s)<script.*?>(.*?)</script>', response.lower())
    for match in matches:
        if xsschecker in match:
            scripts.append(match)
    return scripts
