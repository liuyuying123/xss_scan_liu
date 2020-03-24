#各种要用到的小函数
import json
import random
import re
from urllib.parse import urlparse

import config
from config import xsschecker




#提取response中的<script>标签
def extractScripts(response):
    scripts = []
    matches = re.findall(r'(?s)<script.*?>(.*?)</script>', response.lower())
    for match in matches:
        if xsschecker in match:
            scripts.append(match)
    return scripts



#从带参数的URL中将主URL参数提取出来
def getUrl(url, GET):
    if GET:
        return url.split('?')[0]
    else:
        return url

def getVar(name):
    return config.globalVariables[name]





def getParams(url, data, GET):
    params = {}
    if '=' in url:
        data = url.split('?')[1]
        if data[:1] == '?':
            data = data[1:]
    elif data:
        if getVar(jsondata) or getVar(path):
            params = data
        else:
            try:
                params = json.loads(data.replace('\'', '"'))
                return params
            except json.decoder.JSONDecodeError:
                pass
    else:
        return None
    #如果URL中不带参数，而是使用post请求
    if not params:
        #有这种情况，比如data是一个字符串，data='name=admin&password=admin'
        parts = data.split('&')
        for part in parts:
            each = part.split('=')
            if len(each) < 2:
                each.append('')
            try:
                params[each[0]] = each[1]
            except IndexError:
                params = None

    #返回的是一个Param字典
    return params



def converter(data, url=False):
    if 'str' in str(type(data)):#如果传入的data是json数据
        if url:
            dictized = {}
            parts = data.split('/')[3:]
            for part in parts:
                dictized[part] = part
            return dictized#返回字典
        else:
            return json.loads(data)#此时的data是json字符串，将json类型的数据转换成dict字典
    else:#如果data不是json格式，是字典的话
        if url:
            url = urlparse(url).scheme + '://' + urlparse(url).netloc
            for part in list(data.values()):
                url += '/' + part
            return url
        else:
            return json.dumps(data)#将data转换为json结构



#生成攻击向量
def genGen(fillings, eFillings, lFillings, eventHandlers, tags, functions, ends, badTag=None):
    vectors = []
    r = randomUpper  # randomUpper randomly converts chars of a string to uppercase
    for tag in tags:
        if tag == 'd3v' or tag == 'a':
            bait = xsschecker
        else:
            bait = ''
        for eventHandler in eventHandlers:
            # if the tag is compatible with the event handler
            if tag in eventHandlers[eventHandler]:
                for function in functions:
                    for filling in fillings:
                        for eFilling in eFillings:
                            for lFilling in lFillings:
                                for end in ends:
                                    if tag == 'd3v' or tag == 'a':
                                        if '>' in ends:
                                            end = '>'  # we can't use // as > with "a" or "d3v" tag
                                    breaker = ''
                                    if badTag:
                                        breaker = '</' + r(badTag) + '>'
                                    vector = breaker + '<' + r(tag) + filling + r(
                                        eventHandler) + eFilling + '=' + eFilling + function + lFilling + end + bait
                                    vectors.append(vector)
    return vectors


def randomUpper(string):
    return ''.join(random.choice((x, y)) for x, y in zip(string.upper(), string.lower()))



def stripper(string, substring, direction='right'):
    done = False
    strippedString = ''
    if direction == 'right':
        string = string[::-1]
    for char in string:
        if char == substring and not done:
            done = True
        else:
            strippedString += char
    if direction == 'right':
        strippedString = strippedString[::-1]
    return strippedString












