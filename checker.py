import copy
from fuzzywuzzy import fuzz#进行模糊匹配的库
import re
from requester import requester
from urllib.parse import unquote
from config import xsschecker


def checker(url,params,headers,GET,delay,payload,positions,timeout,encoding):
    checkString='st4r7s'+payload+'3nd'
    if encoding:
        checkString=encoding(unquote(checkString))#urlencode逆向
    response=requester(url,replaceValue(params,xsschecker,checkString,copy.deepcopy),headers,GET,delay,timeout).text.lower()
    reflectedPositions=[]
    for match in re.finditer('st4r7s',response):
        reflectedPositions.append(match.start())#将找到匹配位置的字符位置标记
    filledPositions=fillHoles(positions,reflectedPositions)#fillHoles函数的用法：
    #填补哪些被完全过滤的位置，例如有些网站就是你提交了危险字符，他会拦截你整个字符串，这样我们的输出在扫描器看来就会少了一处
    #也就是reflectedPositions 长度比positions小

    #Itretating over the reflections
    num=0
    efficiences=[]
    for position in filledPositions:
        allEfficiencies=[]
        try:
            reflected=response[reflectedPositions[num]:reflectedPositions[num]+len(checkString)]
            #打分的地方就是这里，fuzz.partial_ratio是一个比较字符串函数
            efficiency=fuzz.partial_ratio(reflected,checkString.lower())
            allEfficiencies.append(efficiency)
        except IndexError:
            pass

        if position:
            reflected=response[position:position+len(checkString)]
            if encoding:
                checkString=encoding(checkString.lower())
            efficiency=fuzz.partial_ratio(reflected,checkString)
            if reflected[:-2]==('\\%s' %checkString.replace('st4r7s','').replace('3nd','')):
                efficiency=90
            allEfficiencies.append(efficiency)
            efficiences.append(max(allEfficiencies))
        else:
            efficiences.append(0)
            num+=1
    return list(filter(None,efficiences))#过滤掉0 或者''



def replaceValue(mapping,old,new,strategy=None):
    anotherMap=strategy(mapping) if strategy else mapping
    if old in anotherMap.values():
        for k in anotherMap.keys():
            if anotherMap[k]==old:
                anotherMap[k]=new
    return anotherMap



def fillHoles(original, new):
    filler = 0
    filled = []
    for x, y in zip(original, new):
        if int(x) == (y + filler):
            filled.append(y)
        else:
            filled.extend([0, y])
            filler += (int(x) - y)
    return filled

















